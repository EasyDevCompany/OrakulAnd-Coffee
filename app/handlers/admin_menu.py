from dependency_injector.wiring import Provide, inject

from aiogram.utils.markdown import hbold
from loader import bot
from aiogram import types, Dispatcher
from app.utils.states.send_post import WaitePostInformation
from app.utils.states.add_card import AddCard

from aiogram.dispatcher import FSMContext
from app.core.containers import Container

from app.utils.keyboards import keyboards
from app.services.telegram_user_service import TelegramUserService
from app.services.card_service import CardService


async def admin_start(message: types.Message):
    user_id = message.from_user.id
    if user_id == 688136452 or user_id == 257787369 or user_id == 5217389680:
        await message.answer('Выберите один пункт из меню ниже:', reply_markup=keyboards.new_users_keyboard)


@inject
async def users_count_info(
        callback_query: types.CallbackQuery,
        telegram_user_service: TelegramUserService = Provide[Container.telegram_user_service]
):
    count = await telegram_user_service.get_user_count()
    await callback_query.message.edit_reply_markup()
    await callback_query.message.answer(f"Всего пользователей в боте: {count[0]}")


@inject
async def last_month(
        callback_query: types.CallbackQuery,
        telegram_user_service: TelegramUserService = Provide[Container.telegram_user_service]
):
    await callback_query.message.delete_reply_markup()
    users = await telegram_user_service.last_month_user()
    for user in users:
        await callback_query.answer(
            f"Пользователь: {user.first_name}\n"
            f"Дата регистрации: {user.registration_date}\n"
            f"Имя пользователя: {user.username}"
        )


@inject
async def last_week(
        callback_query: types.CallbackQuery,
        telegram_user_service: TelegramUserService = Provide[Container.telegram_user_service]
):
    await callback_query.message.delete_reply_markup()
    users = await telegram_user_service.last_week_user()
    for user in users:
        await callback_query.answer(
            f"Пользователь: {user.first_name}\n"
            f"Дата регистрации: {user.registration_date}\n"
            f"Имя пользователя: {user.username}"
        )


@inject
async def last_day(
        callback_query: types.CallbackQuery,
        telegram_user_service: TelegramUserService = Provide[Container.telegram_user_service]
):
    await callback_query.message.delete_reply_markup()
    users = await telegram_user_service.last_day_user()
    for user in users:
        await callback_query.answer(
            f"Пользователь: {user.first_name}\n"
            f"Дата регистрации: {user.registration_date}\n"
            f"Имя пользователя: {user.username}"
        )


async def chose_time(callback_query: types.CallbackQuery):
    await callback_query.message.edit_reply_markup()
    await callback_query.message.answer(f"Выберите промежуток времени:", reply_markup=keyboards.stat_keyboard)


async def add_post(callback_query: types.CallbackQuery):
    await callback_query.message.edit_reply_markup()
    await callback_query.message.answer('Отправьте боту текст:', reply_markup=keyboards.cancel_keyboard)
    await WaitePostInformation.waite_description.set()


async def save_description(message: types.Message, state: FSMContext):
    await state.update_data(description=message.text)
    await message.answer("Добавить фотографию к посту?", reply_markup=keyboards.yes_or_no)
    await WaitePostInformation.waite_image_answer.set()


@inject
async def waite_image_answer(
        callback_query: types.CallbackQuery,
        state: FSMContext,
        telegram_user_service: TelegramUserService = Provide[Container.telegram_user_service]
):
    if callback_query.data == "cancel":
        await state.finish()
        await callback_query.message.answer("Отменено!")
    await callback_query.message.delete_reply_markup()
    user_data = await state.get_data()
    image_answer = callback_query.data
    if image_answer == "yes":
        await callback_query.message.answer("Отправьте боту изображение:", reply_markup=keyboards.cancel_keyboard)
        await WaitePostInformation.waite_image.set()
    elif callback_query.data == "no":
        users = await telegram_user_service.list()
        description = user_data["description"]
        for user in users:
            try:
                await bot.send_message(user.user_id, f"{description}")
            except Exception as exc:
                print(f"{exc}")
        await state.finish()


@inject
async def save_image_and_post(
        message: types.Message,
        state: FSMContext,
        telegram_user_service: TelegramUserService = Provide[Container.telegram_user_service]
):
    image = message.photo[0].file_id
    user_data = await state.get_data()
    users = await telegram_user_service.list()
    description = user_data["description"]
    for user in users:
        try:
            await bot.send_photo(user.user_id, image, f"{description}")
        except Exception as exc:
            print(f'{exc} -- {user.user_id} {user.username} - этот пользователь заблокировал бота')
    await state.finish()


async def cancel_btn(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.edit_reply_markup()
    await callback_query.message.answer('Отменено!')
    await state.finish()


async def add_card(message: types.Message):
    user_id = message.from_user.id
    if user_id == 688136452:
        await message.answer('Отправьте боту изображение карты!')
        await AddCard.waite_card_images.set()
    else:
        print(f'Пользователь с ID:{user_id} попытался добавить карту!')


async def save_card_image(message: types.Message, state: FSMContext):
    image = message.photo[0].file_id
    print(f'Добавлено фото: {image}')
    await state.update_data(image=image)
    await message.answer('Отправьте название карты:')
    await AddCard.waite_card_title.set()


async def save_tittle(message: types.Message, state: FSMContext):
    title = message.text
    await state.update_data(title=title)
    print(f'Название карты: {title}')
    await message.answer(f'Отправьте боту описание карты:')
    await AddCard.waite_card_description.set()


async def save_card(
        message: types.Message,
        state: FSMContext,
        card_service: CardService = Provide[Container.card_service]
):
    user_data = await state.get_data()
    description = message.text
    new_card = await card_service.add_card(
        image=user_data["image"],
        card_title=user_data["title"],
        card_description=description,
    )

    await message.answer('Новая карта сохранена!')
    await state.finish()


def register_admin_menu_handler(dp: Dispatcher):
    dp.register_message_handler(admin_start, commands=["admin"])
    dp.register_callback_query_handler(users_count_info, text="users_count")
    dp.register_callback_query_handler(chose_time, text="new_users")
    dp.register_callback_query_handler(last_month, text="one_mouth")
    dp.register_callback_query_handler(last_week, text="one_week")
    dp.register_callback_query_handler(last_day, text="last_day")
    dp.register_callback_query_handler(add_post, text='add_post')
    dp.register_message_handler(save_description, state=WaitePostInformation.waite_description)
    dp.register_message_handler(waite_image_answer, state=WaitePostInformation.waite_image_answer)
    dp.register_message_handler(
        save_image_and_post,
        state=WaitePostInformation.waite_image,
        content_types=types.ContentTypes.PHOTO
    )
    dp.register_message_handler(cancel_btn, text="cancel", state="*")
    dp.register_message_handler(add_card, commands=['add_card'])
    dp.register_message_handler(save_card_image,
                                state=AddCard.waite_card_images,
                                content_types=types.ContentTypes.PHOTO)
    dp.register_message_handler(save_tittle, state=AddCard.waite_card_title)
    dp.register_message_handler(save_card, state=AddCard.waite_card_description)

