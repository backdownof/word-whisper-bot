from aiogram import types, Router, F
from sqlalchemy import func, select, not_, join, and_, outerjoin, or_
import transaction


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
    
    subquery = select(
        models.UserWord
    ).where(
        models.UserWord.user_id == user.id,
        models.UserWord.list_added.is_(True)
    ).with_only_columns(
        models.UserWord.word_id
    )

    word_and_translation = models.DBSession.execute(select(
        models.Word,
        models.WordTranslation
    ).join(
        models.WordTranslation,
        models.WordTranslation.word_id == models.Word.id,
    ).where(
        models.Word.level.in_(user_levels)
    ).where(
        models.Word.id.notin_(subquery)
    ).order_by(
        func.random()
    )).first()

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
    new_user_word.add()
    transaction.commit()
    word = models.Word.query.get(word_id)
    word = word.word
    
    await message_helpers.send_message(
        event=event,
        text=f'Слово <b>{word}</> добавлено в карточки для изучения!',
        reply_markup=kb,
    )
