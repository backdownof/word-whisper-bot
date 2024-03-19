from db import models
from views.constants.buttons import Button
from views.constants.callbacks import Callback
from views.constants.messages import Message
from views.constants.buttons import WordLevelButton
from views.helpers import messages as message_helpers, keyboard as kb_helpers

from sqlalchemy import func


async def send_daily_word_to_user(user: models.User):
    keyboard_data = [
        (Button.NEXT_WORD, Callback.NEXT_WORD),
        (Button.SETTINGS, Callback.SETTINGS),
    ]
    kb = kb_helpers.build_inline_keyboard(keyboard_data, adjust_num=2)

    user_levels = [WordLevelButton.ALL[idx] for idx in user.selected_levels]
    if len(WordLevelButton.ALL) in user_levels:
        user_levels.append('')

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
        await message_helpers.send_message(
            text=Message.NO_NEW_WORDS,
            reply_markup=kb,
            user=user
        )
        return

    message = message_helpers.MessageTemplates.get_new_word_message(word_and_translation)

    await message_helpers.send_message(
        text=message,
        reply_markup=kb,
        user=user
    )
