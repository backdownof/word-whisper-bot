import transaction

from db import models
from views.constants.buttons import Button
from views.constants.callbacks import Callback
from views.constants.messages import Message
from views.helpers import messages as message_helpers, keyboard as kb_helpers

from aiogram import types, Router, F
from sqlalchemy import tablesample
from sqlalchemy.orm import aliased

router = Router()


@router.callback_query(F.data == Callback.NEXT_WORD)
async def new_word(event: types.Message):
    keyboard_data = [
        (Button.NEXT_WORD, Callback.NEXT_WORD),
        (Button.SETTINGS, Callback.SETTINGS),
    ]
    kb = kb_helpers.build_inline_keyboard(keyboard_data, adjust_num=2)

    random_word_alias = aliased(
        models.Word,
        tablesample(models.Word, 2.5)
    )
    word_and_translation: models.WordExamples = models.DBSession.query(
        random_word_alias,
        models.WordTranslation
    ).join(
        models.WordTranslation,
        models.WordTranslation.word_id == random_word_alias.id,
    ).limit(1).first()

    if not word_and_translation:
        await message_helpers.send_message(event, Message.NO_NEW_WORDS, reply_markup=kb)
        return

    message = message_helpers.MessageTemplates.get_new_word_message(word_and_translation)

    await message_helpers.send_message(event, message, reply_markup=kb)
