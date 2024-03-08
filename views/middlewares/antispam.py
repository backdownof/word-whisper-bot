import logging

from typing import Any, Awaitable, Callable, Dict
from aiogram import BaseMiddleware
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import TelegramObject, Message

logger = logging.getLogger(__name__)


class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self, storage: RedisStorage):
        self.storage = storage

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        user = f'user_{event.from_user.id}'

        check_user = await self.storage.redis.get(name=user)

        if check_user:
            if (int(check_user.decode()) == 1):
                await self.storage.redis.set(name=user, value=0, ex=1)
                return await event.answer(
                    "Мы обнаружили слишком частую отправку сообщений. Попробуйте повторить запрос позже."
                )
            return

        await self.storage.redis.set(name=user, value=1, ex=1)
        logger.info(f"К пользователю ({user}) был добавлен применен антиспам фильтр")

        return await handler(event, data)
