import os
import re
import transaction
from typing import List

from db import models
from views.constants.buttons import Button
from views.helpers import messages as message_helpers
from sqlalchemy.sql import text

from aiogram import Bot, types, Router, F
from aiogram.filters.command import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.fsm.context import FSMContext
from dotenv import load_dotenv

load_dotenv('.env')
BOT_TOKEN = os.environ.get('BOT_TOKEN')

router = Router()


@router.message(Command("start"))
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

    # buttons = [Button.CREATE_CHAR]
    # kb = [[types.KeyboardButton(text=button_text)] for button_text in buttons]

    # keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

    rand_id = models.DBSession.execute(text(
        '''
        SELECT id
        FROM words TABLESAMPLE SYSTEM (1)
        WHERE id != 5
        ORDER BY word LIMIT 1;
        '''
    )).fetchone()[0]
    rand_word: models.Word = models.Word.query.get(rand_id)
    examples: List[models.WordExamples] = models.DBSession.query(
        models.WordExamples
    ).filter(
        models.WordExamples.word_id == rand_id
    ).limit(2).all()

    messasge = ((
        f"Слово: <b>{rand_word.word.capitalize()}</b>\n"
        f"Перевод: <b>{rand_word.translate_ru.capitalize()}</b>\n"
    ))

    if examples:
        messasge += "<b>Примеры:</b>\n"

    for example in examples:
        messasge += f"<i>- {example.example_sentece}</i>\n"

    await message_helpers.send_message(event, messasge)


# @router.message(lambda msg: msg.text == Button.TRAVEL_TO)
# async def travel_to_button_pressed(event: types.Message):
#     character = Character(user_id=event.from_user.id)

#     location = LocationModel(character=character)
#     near_locations = location.get_near_locations()

#     if not near_locations:
#         await event.answer(
#             text="Увы, но от сюда путешествовать некуда.\n"
#             "Пожалуйста, сообщите Админам игры. Мы постараемся помочь как можно скорее."
#         )
#         return

#     kb_builder = ReplyKeyboardBuilder()
#     for location_name, location_info in near_locations.items():
#         button = types.KeyboardButton(
#             text='{near_location} ({time_to_travel} сек)'.format(
#                 near_location=location_name,
#                 time_to_travel=location_info['time_to_travel']
#             )
#         )
#         kb_builder.add(button)

#     button = kb_builder.add(types.KeyboardButton(text=Buttons.BACK))
#     kb_builder.adjust(2)

#     await event.answer(
#         text='''Куда хотите отправиться?''',
#         reply_markup=kb_builder.as_markup(resize_keyboard=True)
#     )
