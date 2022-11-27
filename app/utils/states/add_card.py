from aiogram.dispatcher.filters.state import State, StatesGroup


class AddCard(StatesGroup):
    waite_card_images = State()
    waite_card_title = State()
    waite_card_description = State()