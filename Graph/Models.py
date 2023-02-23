class StateFieldsConsts():
    NAME                = 'Название'
    FORMS               = 'Форма'
    IN_TRANSITIONS      = 'Входящие переходы'
    OUT_TRANSITIONS     = 'Выходящие переходы'


class TransitionFieldConsts():
    NAME                = 'Название'
    SOURCE              = 'Откуда'
    TARGET              = 'Куда'
    FORM_CONDITIONS     = 'Эллемент формы'
    TRANSITION_CONDITION= 'Условие перехода'


class TransitionTypesConsts():
    CONDITIONAL     = 'По формам'
    STRICT          = 'Закончить все формы'
    UNCONDITIONAL   = 'Без условия'


class FormFieldConsts():
    NAME                = 'Название'
    TYPE                = 'Тип'
    STATE_ID            = 'Состояние'
    TAGS                = 'jinja tags'

