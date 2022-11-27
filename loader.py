from app.core.config import settings


from aiogram import Dispatcher, types, Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage

bot = Bot(token=settings.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
# bot = Bot(token="5741872024:AAHxkE3O3MmL8zDN7c_oYIQy7tAAg8aKDLw", parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=MemoryStorage())
