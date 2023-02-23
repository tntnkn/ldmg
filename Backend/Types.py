from enum        import Enum, auto, unique
from dataclasses import dataclass


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


class FormElemsTypes():
    text            = 'TEXT'
    form            = 'FORM'
    d_form_chief    = 'D_FORM_CHIEF'
    d_form          = 'D_FORM'
    button          = 'BUTTON'
    s_choice        = 'S_CHOICE'
    m_choice        = 'M_CHOICE'


class BranchTypes():
    CONDITIONAL     = 'CONDITIONAL'
    STRICT          = 'STRICT'
    UNCONDITIONAL   = 'UNCONDITIONAL'

