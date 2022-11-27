import logging
import tasks
from aiogram.utils import executor
from aiogram import Dispatcher

from loader import dp

from app.db.base import Base
from app.db.session import engine

from app.handlers import cards, admin_menu

from app.core.containers import Container

from app import middlewares

from app.models.user import TelegramUser
from app.models.card import Card

cards.register_card_handler(dp=dp)
admin_menu.register_admin_menu_handler(dp=dp)


def on_startup(dispatcher: Dispatcher):
    Base.metadata.create_all(bind=engine)
    middlewares.setup(dp=dispatcher)


if __name__ == "__main__":
    logging.basicConfig(
        format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s',
        level=logging.INFO,
    )
    container = Container()
    container.wire(modules=[cards, admin_menu, tasks])
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup(dispatcher=dp))
