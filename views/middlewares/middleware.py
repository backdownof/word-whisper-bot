from typing import Any, Awaitable, Callable, Dict

from db import models

import transaction
from aiogram import BaseMiddleware
from aiogram import types


class MessageMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[types.Message, Dict[str, Any]], Awaitable[Any]],
        event: types.Message,
        data: Dict[str, Any]
    ) -> Any:
        user = models.User.get_by_tg_id(event.from_user.id)
        if not user:
            user = models.User(
                full_name=event.from_user.full_name,
                tg_id=event.from_user.id,
                tg_nickname=event.from_user.username,
            )
            user.add()

            transaction.commit()
            user.add()

        data['user'] = user

        return await handler(event, data)
