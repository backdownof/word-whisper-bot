from views.constants import buttons


class Message:
    WELCOME_MESSAGE = (
        "<b>WordWhisperBot</b> приветствует вас!\n"
        f"Чтобы выучить новое слово, нажмите кнопку [<b>{buttons.Button.NEXT_WORD}</b>]\n\n"
        f"Вы можете пометить слово, как [<b>{buttons.Button.ALREADY_KNOW}</b>], [<b>{buttons.Button.ADD_TO_LEARNING}</b>]\n\n"
        f"Для быстрого перевода слова или фразы, отправьте слово или фразу текстом.\n\n"
        "В настройках вы можете выбрать желаемые уровни сложности предлагаемых слов.\n"
        "Доступные уровни:\n"
        f"- {buttons.WordLevelButton.A1}, {buttons.WordLevelButton.A2}\n"
        f"- {buttons.WordLevelButton.B1}, {buttons.WordLevelButton.B2}\n"
        f"- {buttons.WordLevelButton.C1}, {buttons.WordLevelButton.C2}\n"
        f"- {buttons.WordLevelButton.UKNOWN_TEXT} (этот уровень не был определен автоматически)\n"
        f"- {buttons.WordLevelButton.SELECT_ALL}\n\n"
        "Также вы можете помочь улучшить перевод слов, примеров, предложить новое слово или словосочетание, или добавить примеры к уже существующим словам.\n"
        f"Нажмите кнопку <b>{buttons.Button.EDIT}</b> во время изучения слов.\n\n"
        f"В настройках вы можете выбрать, в какое время вам присылать новое слово для изучения. "
        "Или совсем отключить функцию автоматической отправки новых слов для изучения.\n"
    )

    NO_LEVEL_SELECTED = "Не выбран ни один уровень для изучения. Проверьте настройки и выберите желаемые уровни слов."

    NO_NEW_WORDS = "К сожалению, новых слов для изучения нет (или возникла ошибка). Попробуйте позже"

    NO_SUCH_MENU_YET = "Данное меню на текущий момент не реализовано"

    SETTINGS = "Выберите нужное меню настроек"

    CANNOT_TRANSLATE_LONG = "Переводчик пока не умеет переводить сообщения больше 300 символов"
