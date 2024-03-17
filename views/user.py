from db import models
from views.constants.buttons import Button, WordLevelButton
from views.constants.callbacks import Callback as callback_const
from views.constants.commands import Command as command_const
from views.constants.messages import Message
from views.helpers import messages as message_helpers, keyboard as kb_helpers

import transaction
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
    keyboard_data = kb_helpers.get_user_level_settings_keyboard(user)
    kb = kb_helpers.build_inline_keyboard(keyboard_data, adjust_num=2)

    await message_helpers.send_message(event, Message.SETTINGS, reply_markup=kb)


@router.callback_query(F.data.regexp(f"^{callback_const.WORD_LEVEL_SELECTED}_\d+$"))
async def user_word_level_selected(callback: types.CallbackQuery, user: models.User):
    selected_level = int(
        callback.data.removeprefix(
            callback_const.WORD_LEVEL_SELECTED
        ).split('_', 1)[1]
    )

    if selected_level == int(callback_const.ALL_WORD_LEVELS):
        user.level_settings = ','.join([str(idx) for idx, _ in enumerate(WordLevelButton.ALL)])
    elif selected_level in user.selected_levels:
        user.level_settings = ','.join(str(idx) for idx in user.selected_levels if idx != selected_level)
    else:
        user.level_settings = f"{user.level_settings},{selected_level}" if user.level_settings else str(selected_level)

    user.add()

    keyboard_data = kb_helpers.get_user_level_settings_keyboard(user)
    kb = kb_helpers.build_inline_keyboard(keyboard_data, adjust_num=2)

    transaction.commit()

    await message_helpers.send_message(callback, Message.SETTINGS, reply_markup=kb)
