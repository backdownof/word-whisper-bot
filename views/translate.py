from __future__ import absolute_import, unicode_literals

from db import models
from async_tasks.periodic.tasks import translate_phrase

from aiogram import types, Router

router = Router()


@router.message()
async def start_handler(event: types.Message, user: models.User):
    translate_phrase.delay(event.text, user.id)
