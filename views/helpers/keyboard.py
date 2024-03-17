from typing import List

from db import models
from views.constants.buttons import Button, WordLevelButton
from views.constants.callbacks import Callback as callback_const

from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder


def build_inline_keyboard(buttons: List[tuple], adjust_num: int = None):
    ikb = InlineKeyboardBuilder()

    for button_text, callback in buttons:
        ikb.add(types.InlineKeyboardButton(
            text=button_text,
            callback_data=callback
        ))

    if adjust_num:
        ikb.adjust(adjust_num)

    return ikb.as_markup()


def get_user_level_settings_keyboard(user: models.User):
    keyboard_data = []
    for idx, level_button in enumerate(WordLevelButton.ALL):
        selected = "✅ " if idx in user.selected_levels else ""
        button_text = f"{selected}{level_button or WordLevelButton.UKNOWN_TEXT}"
        button_callback = f"{callback_const.WORD_LEVEL_SELECTED}_{idx}"

        keyboard_data.append((button_text, button_callback))

    keyboard_data.append((Button.MENU, callback_const.NEXT_WORD))

    return keyboard_data
