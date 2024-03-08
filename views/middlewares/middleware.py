from typing import Any, Awaitable, Callable, Dict

from db import models
from db.models import DBSession
from views.user import start_handler

from aiogram import BaseMiddleware
from aiogram import types


class MessageMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[types.Message, Dict[str, Any]], Awaitable[Any]],
        event: types.Message,
        data: Dict[str, Any]
    ) -> Any:
        tg_id = event.from_user.id
        player = DBSession.query(
            models.User
        ).filter(
            models.User.tg_id == tg_id
        ).first()

        if not player:
            return await start_handler(event=event)

        return await handler(event, data)
