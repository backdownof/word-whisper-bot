import os
import transaction

from db import models
from views.constants.buttons import Button
from views.constants.callbacks import Callback
from views.constants.commands import Command as c
from views.constants.messages import Message
from views.helpers import messages as message_helpers, keyboard as kb_helpers

from aiogram import types, Router
from aiogram.filters.command import Command

router = Router()


@router.message(Command(c.START))
async def start_handler(event: types.Message):
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

    keyboard_data = [
        (Button.NEXT_WORD, Callback.NEXT_WORD),
        (Button.REPEAT_WORDS, Callback.REPEAT_WORDS),
        (Button.SETTINGS, Callback.SETTINGS),
        (Button.TRANSLATE, Callback.TRANSLATE),
    ]
    kb = kb_helpers.build_inline_keyboard(keyboard_data, adjust_num=2)

    await message_helpers.send_message(event, Message.WELCOME_MESSAGE, reply_markup=kb)
