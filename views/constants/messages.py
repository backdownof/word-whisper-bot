from views.constants import buttons, words


class Message:
    WELCOME_MESSAGE = (
        "WordWhisperBot приветствует вас!\n"
        f"Чтобы выучить новое слово, нажмите кнопку [{buttons.Button.NEXT_WORD}]\n\n"
        f"Вы можете пометить слово, как [{buttons.Button.ALREADY_KNOW}], [{buttons.Button.ADD_TO_LEARNING}]\n\n"
        f"Для быстрого перевода слова или фразы, отправьте слово или фразу текстом.\n\n"
        "В настройках вы можете выбрать желаемые уровни сложности предлагаемых слов.\n"
        "Доступные уровни:\n"
        f"- {words.WordLevel.A1}, {words.WordLevel.A2}\n"
        f"- {words.WordLevel.B1}, {words.WordLevel.B2}\n"
        f"- {words.WordLevel.C1}, {words.WordLevel.C2}\n"
        f"- {words.WordLevel.UNKNOWN} (этот уровень не был определен автоматически)\n"
        f"- {words.WordLevel.ALL}\n\n"
        "Также вы можете помочь улучшить перевод слов, примеров, предложить новое слово или словосочетание, или добавить примеры к уже существующим словам.\n"
        f"Нажмите кнопку {buttons.Button.EDIT} во время изучения слов.\n\n"
        f"В настройках вы можете выбрать, в какое время вам присылать новое слово для изучения. "
        "Или совсем отключить функцию автоматической отправки новых слов для изучения.\n"
    )
