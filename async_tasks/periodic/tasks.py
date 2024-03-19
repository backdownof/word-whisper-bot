import logging
import asyncio

from config import App
from db import models
from views.constants.buttons import Button
from views.constants.callbacks import Callback
from views.constants.messages import Message
from views.constants.words import TranslationLanguage
from views.helpers import messages as message_helpers, keyboard as kb_helpers
from async_tasks.helpers.messages import send_daily_word_to_user

from celery import shared_task, states

logger = logging.getLogger(__name__)


@shared_task(bind=True, soft_time_limit=20)
def send_daily_word(self):
    users_subscribed_query = models.DBSession.query(
        models.User
    ).filter(
        models.User.word_of_day_subscribed.is_(True)
    )

    loop = asyncio.get_event_loop()

    loop.run_until_complete(run_user_cycle(users_subscribed_query))
    self.update_state(state=states.SUCCESS)


async def run_user_cycle(users_subscribed_query):
    async with asyncio.TaskGroup() as tg:
        for user in users_subscribed_query:
            tg.create_task(send_daily_word_to_user(user))


@shared_task
def translate_phrase(word, user_id):
    user = models.User.query.get(user_id)

    keyboard_data = [
        (Button.NEXT_WORD, Callback.NEXT_WORD),
        (Button.SETTINGS, Callback.SETTINGS),
    ]
    kb = kb_helpers.build_inline_keyboard(keyboard_data, adjust_num=2)

    loop = asyncio.get_event_loop()
    if len(word) > 300:
        loop.run_until_complete(
            message_helpers.send_message(
                text=Message.CANNOT_TRANSLATE_LONG,
                reply_markup=kb,
                user=user
            )
        )
        return

    word_and_translation: models.WordExamples = models.DBSession.query(
        models.Word,
        models.WordTranslation
    ).join(
        models.WordTranslation,
        models.WordTranslation.word_id == models.Word.id,
    ).filter(
        models.Word.word == word
    ).first()

    if word_and_translation:
        message = message_helpers.MessageTemplates.get_new_word_message(word_and_translation)

        loop.run_until_complete(
            message_helpers.send_message(
                text=message,
                reply_markup=kb,
                user=user
            )
        )
        return

    prefix = 'translate to ru: ' + word
    input_ids = App.tokenizer(prefix, return_tensors="pt").input_ids
    language_ids = App.model.generate(input_ids)
    tr = App.tokenizer.decode(language_ids[0], skip_special_tokens=True)

    ru_translate = tr or ''

    w = models.Word(
        word=word,
        level='',
        meaning=''
    )
    w.add()
    w.flush()

    word_translation = models.WordTranslation(
        word_id=w.id,
        language=TranslationLanguage.RU,
        translation=ru_translate
    )
    word_translation.add()

    message = message_helpers.MessageTemplates.get_new_word_message((w, word_translation))

    loop.run_until_complete(
        message_helpers.send_message(
            text=message,
            reply_markup=kb,
            user=user
        )
    )
