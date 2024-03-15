from db import models
from views.constants.buttons import Button, WordLevelButton
from views.constants.callbacks import Callback as callback_const
from views.constants.commands import Command as command_const
from views.constants.messages import Message
from views.helpers import messages as message_helpers, keyboard as kb_helpers

from aiogram import types, Router, F
from aiogram.filters.command import Command

router = Router()


@router.message(Command(command_const.START))
async def start_handler(event: types.Message):
    keyboard_data = [
        (Button.NEXT_WORD, callback_const.NEXT_WORD),
        (Button.REPEAT_WORDS, callback_const.REPEAT_WORDS),
        (Button.SETTINGS, callback_const.SETTINGS),
        (Button.TRANSLATE, callback_const.TRANSLATE),
    ]
    kb = kb_helpers.build_inline_keyboard(keyboard_data, adjust_num=2)

    await message_helpers.send_message(event, Message.WELCOME_MESSAGE, reply_markup=kb)


@router.callback_query(F.data == callback_const.SETTINGS)
async def user_settings(event: types.Message):
    keyboard_data = [
        (Button.WORD_LEVEL_SETTINGS, callback_const.WORD_LEVEL_SETTINGS),
        (Button.NOTIFICATION_SETTINGS, callback_const.NOTIFICATION_SETTINGS),
        (Button.MENU, callback_const.NEXT_WORD),
    ]
    kb = kb_helpers.build_inline_keyboard(keyboard_data, adjust_num=1)

    await message_helpers.send_message(event, Message.SETTINGS, reply_markup=kb)


@router.callback_query(F.data == callback_const.NOTIFICATION_SETTINGS)
async def user_notification_settings(event: types.Message):
    keyboard_data = [(Button.MENU, callback_const.NEXT_WORD)]
    kb = kb_helpers.build_inline_keyboard(keyboard_data, adjust_num=1)

    await message_helpers.send_message(event, Message.NO_SUCH_MENU_YET, reply_markup=kb)


@router.callback_query(F.data == callback_const.WORD_LEVEL_SETTINGS)
async def user_word_level_settings(event: types.Message, user: models.User):
    level_indexes = [int(level_idx_str) for level_idx_str in user.level_settings.split(',')]

    keyboard_data = []
    for idx, level_button in enumerate(WordLevelButton.ALL):
        selected = "✅ " if idx in level_indexes else ""
        button_text = f"{selected}{level_button}"
        button_callback = f"{callback_const.WORD_LEVEL_SELECTED}_{idx}"

        keyboard_data.append((button_text, button_callback))

    if not level_indexes:
        button_text = WordLevelButton.SELECT_ALL
        button_callback = f"{callback_const.WORD_LEVEL_SELECTED}_{callback_const.ALL_WORD_LEVELS}"
        keyboard_data.append((button_text, button_callback))

    keyboard_data.append((Button.MENU, callback_const.NEXT_WORD))

    kb = kb_helpers.build_inline_keyboard(keyboard_data, adjust_num=2)

    await message_helpers.send_message(event, Message.SETTINGS, reply_markup=kb)
