import asyncio

from aiogram import types, Dispatcher
from aiogram.dispatcher import DEFAULT_RATE_LIMIT
from aiogram.dispatcher.handler import CancelHandler, current_handler
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.utils.exceptions import Throttled


class ThrottlingMiddleware(BaseMiddleware):

    def __init__(self, limit=DEFAULT_RATE_LIMIT, key_prefix='antiflood_'):
        self._rate_limit = limit
        self._prefix = key_prefix
        super(ThrottlingMiddleware, self).__init__()

    async def on_process_message(self, message: types.Message, data: dict):
        handler = current_handler.get()
        dispatcher = Dispatcher.get_current()
        if handler:
            limit = getattr(handler, 'throttling_rate_limit', self._rate_limit)
            key = getattr(handler, 'throttling_key', f"{self._prefix}_{handler.__name__}")
        else:
            limit = self._rate_limit
            key = f"{self._prefix}_message"
        try:
            await dispatcher.throttle(key, rate=limit)
        except Throttled as t:
            await self.message_throttled(message, t)
            raise CancelHandler()

    async def message_throttled(self, message: types.Message, throttled: Throttled):
        handler = current_handler.get()
        dispatcher = Dispatcher.get_current()
        if handler:
            key = getattr(handler, 'throttling_key', f"{self._prefix}_{handler.__name__}")
        else:
            key = f"{self._prefix}_message"
        delta = throttled.rate - throttled.delta
        if throttled.exceeded_count == 2:
            await message.reply('Слишком ного сообщений боту, сбавьте темп!')
        if throttled.exceeded_count == 3:
            await message.reply('Ответ заблокирован, подождите 10 секунд.')
        await asyncio.sleep(delta)
        thr = await dispatcher.check_key(key)
        if thr.exceeded_count == throttled.exceeded_count:
            await message.reply('Unlocked.')