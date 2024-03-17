import transaction

from db import models
from views.constants.buttons import Button, WordLevelButton
from views.constants.callbacks import Callback
from views.constants.messages import Message
from views.helpers import messages as message_helpers, keyboard as kb_helpers

from aiogram import types, Router, F
from sqlalchemy import func

router = Router()


@router.callback_query(F.data == Callback.NEXT_WORD)
async def new_word(event: types.Message, user: models.User):
    keyboard_data = [
        (Button.NEXT_WORD, Callback.NEXT_WORD),
        (Button.SETTINGS, Callback.SETTINGS),
    ]
    kb = kb_helpers.build_inline_keyboard(keyboard_data, adjust_num=2)

    user_levels = [WordLevelButton.ALL[idx] for idx in user.selected_levels]
    if len(WordLevelButton.ALL) in user_levels:
        user_levels.append('')

    if not user_levels:
        await message_helpers.send_message(event, Message.NO_LEVEL_SELECTED, reply_markup=kb)
        return

    word_and_translation: models.WordExamples = models.DBSession.query(
        models.Word,
        models.WordTranslation
    ).join(
        models.WordTranslation,
        models.WordTranslation.word_id == models.Word.id,
    ).filter(
        models.Word.level.in_(user_levels)
    ).order_by(func.random()).first()

    if not word_and_translation:
        await message_helpers.send_message(event, Message.NO_NEW_WORDS, reply_markup=kb)
        return

    message = message_helpers.MessageTemplates.get_new_word_message(word_and_translation)

    await message_helpers.send_message(event, message, reply_markup=kb)
