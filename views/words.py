# поправил импорты по PEP
from sqlalchemy import func
import transaction

from aiogram import types, Router, F
from db import models
from views.constants.buttons import Button, WordLevelButton
from views.constants.callbacks import Callback
from views.constants.messages import Message
from views.helpers import messages as message_helpers, keyboard as kb_helpers


router = Router()


@router.callback_query(F.data == Callback.NEXT_WORD)
async def new_word(event: types.Message, user: models.User):
    user_levels = [WordLevelButton.ALL[idx] for idx in user.selected_levels]
    if len(WordLevelButton.ALL) in user_levels:
        user_levels.append('')
    if not user_levels:
        await message_helpers.send_message(
            event=event,
            text=Message.NO_LEVEL_SELECTED,
            reply_markup=kb
        )
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
    keyboard_data = [
        (Button.NEXT_WORD, Callback.NEXT_WORD),
        (Button.SETTINGS, Callback.SETTINGS),
        (Button.ADD_LEARNING, f'{Callback.ADD_LEARNING}_{word_and_translation[0].id}')

    ]
    kb = kb_helpers.build_inline_keyboard(keyboard_data, adjust_num=2)    
    if not word_and_translation:
        await message_helpers.send_message(
            event=event,
            text=Message.NO_NEW_WORDS,
            reply_markup=kb
        )
        return

    message = message_helpers.MessageTemplates.get_new_daily_word_message(word_and_translation)

    await message_helpers.send_message(
        event=event,
        text=message,
        reply_markup=kb,
    )

@router.callback_query(F.data.regexp(f"^{Callback.ADD_LEARNING}_\d+$"))
async def add_word(event, user: models.User):
    keyboard_data = [
        (Button.NEXT_WORD, Callback.NEXT_WORD),
        (Button.SETTINGS, Callback.SETTINGS),
        (Button.DELETE_LEARNING, Callback.DELETE_LEARNING)

    ]
    kb = kb_helpers.build_inline_keyboard(keyboard_data, adjust_num=2)
    word_id = event.data.split('_')[-1]
 
    new_user_word = models.UserWord()
    new_user_word.user_id = user.id  
    new_user_word.word_id = word_id  
    new_user_word.learned = False
    new_user_word.list_added = True
    models.DBSession.add(new_user_word)
    transaction.commit()
    word = models.DBSession.query(models.Word).filter_by(id=word_id).first()
    word = word.word
    
    await message_helpers.send_message(
        event=event,
        text = f'Слово <b>{word}</> добавлено в карточки для изучения!',
        reply_markup=kb,
        )
