from enum       import Enum, auto, unique


class FormType():
    UNKNOWN         = 'UNKNOWN TYPE!'
    REGULAR_TEXT    = 'Простой текст'
    REGULAR_FIELD   = 'Поле для заполнения'
    DYNAMIC_FIELD   = 'Поле для заполнения динамическое'
    BUTTON          = 'Кнопка действия'
    SINGLE_CHOICE   = 'Кнопка единичного выбора'
    MULTI_CHOICE    = 'Кнопка множественного выбора'
    DOCUMENT        = 'Документ'
    DEFAULT         = 'По умолчанию' 
    ALWAYS_REACHABLE= 'Всегда доступно'

