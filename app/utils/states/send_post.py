from aiogram.dispatcher.filters.state import State, StatesGroup


class WaitePostInformation(StatesGroup):
    waite_description = State()
    waite_image_answer = State()
    waite_image = State()