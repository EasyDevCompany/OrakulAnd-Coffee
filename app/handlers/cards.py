from loguru import logger
from dependency_injector.wiring import Provide, inject


from aiogram.utils.markdown import hbold
from aiogram import types, Dispatcher

from app.core.containers import Container

from app.utils.keyboards import keyboards

from app.services.telegram_user_service import TelegramUserService
from app.services.users_limit_service import UserLimitService
from app.services.card_service import CardService


@inject
async def welcome_command(
        message: types.Message,
        telegram_user_service: TelegramUserService = Provide[Container.telegram_user_service],
        users_limit_service: UserLimitService = Provide[Container.users_limit_service]

):
    await message.answer(f'{hbold(f"Привет, {message.from_user.first_name}!")}👋\n\n'
                         f'Я-бот, который разложит для тебя оракул с подробным описанием карт!\n'
                         f'{hbold("Как мною пользоваться?")}\n\n'
                         f'Жми на кнопку ниже и получай свою карту👇', reply_markup=keyboards.take_a_card_keyboard)

    await telegram_user_service.create_user(
        user_id=message.from_user.id,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name,
        username=message.from_user.username
    )

    await users_limit_service.create_limits(
        user_id=message.from_user.id
    )


@inject
async def take_card(
        callback_query: types.CallbackQuery,
        card_service: CardService = Provide[Container.card_service],
        users_limit_service: UserLimitService = Provide[Container.users_limit_service]
):
    card = await card_service.get_card()
    await callback_query.message.delete_reply_markup()
    await users_limit_service.update_limits(user_id=callback_query.from_user.id)
    await callback_query.message.answer("Взяли карту")


def register_card_handler(dp: Dispatcher):
    dp.register_message_handler(welcome_command, commands=["start"])
    dp.register_callback_query_handler(take_card, text="take_a_card")
    dp.register_callback_query_handler(take_card, text="take_a_new_card")