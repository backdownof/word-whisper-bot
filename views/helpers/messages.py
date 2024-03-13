from typing import List, Tuple

from db import models

from aiogram import types


async def send_message(event, text, reply_markup=None):
    if isinstance(event, types.CallbackQuery):
        await event.message.edit_text(text, parse_mode='HTML')
        if reply_markup:
            await event.message.edit_reply_markup(reply_markup=reply_markup)
        return

    await event.answer(text, reply_markup=reply_markup, parse_mode='HTML')


class MessageTemplates:
    def get_new_word_message(word_and_translation: Tuple[models.Word, models.WordTranslation]):
        word_to_learn, word_translation = word_and_translation

        message = (
            f"<b>Слово:</b> {word_to_learn.word.capitalize()}\n"
            f"<b>Перевод:</b> {word_translation.translation.capitalize()}\n"
        )

        word_examples: List[models.WordExamples] = models.DBSession.query(
            models.WordExamples
        ).filter(
            models.WordExamples.word_id == word_to_learn.id
        ).limit(2).all()

        if not word_examples:
            return message

        examples = [f"- {word_example.example_sentece}" for word_example in word_examples]

        message += "\n<b>Примеры:</b>\n"
        message += '\n'.join(examples)

        return message
