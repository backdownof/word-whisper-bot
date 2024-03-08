from aiogram import types


async def send_message(event, text, reply_markup=None):
    if isinstance(event, types.CallbackQuery):
        await event.message.edit_text(text, parse_mode='HTML')
        if reply_markup:
            await event.message.edit_reply_markup(reply_markup=reply_markup)
        return

    await event.answer(text, reply_markup=reply_markup, parse_mode='HTML')
