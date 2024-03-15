from typing import List

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
