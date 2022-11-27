from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


take_a_card = InlineKeyboardButton('Получить карту🃏', callback_data='take_a_card')
take_a_new_card = InlineKeyboardButton('Взять еще карту🃏', callback_data='take_a_new_card')
new_users = InlineKeyboardButton("Новые пользователи", callback_data='new_users')
users_count = InlineKeyboardButton("Кол-во пользователей", callback_data='users_count')
send_users_message = InlineKeyboardButton("Сделать рассылку", callback_data="add_post")
one_day = InlineKeyboardButton("За день", callback_data='one_day')
one_week = InlineKeyboardButton("За неделю", callback_data='one_week')
one_mouth = InlineKeyboardButton("За месяц", callback_data='one_mouth')
cancel_btn = InlineKeyboardButton(text="Отменить", callback_data="cancel")
yes = InlineKeyboardButton("Да", callback_data='yes')
no = InlineKeyboardButton("Нет", callback_data='no')


take_a_card_keyboard = InlineKeyboardMarkup().add(take_a_card)
take_a_new_card_keyboards = InlineKeyboardMarkup().add(take_a_new_card)
new_users_keyboard = InlineKeyboardMarkup().add(new_users, users_count).add(send_users_message)
stat_keyboard = InlineKeyboardMarkup().add(one_day, one_week, one_mouth)
cancel_keyboard = InlineKeyboardMarkup().add(cancel_btn)
yes_or_no = InlineKeyboardMarkup().add(yes, no)
