class StateFieldsConsts():
    NAME                = 'Название'
    BEHAVIOR            = 'Поведение'
    FORMS               = 'Форма'
    IN_TRANSITIONS      = 'Входящие переходы'
    OUT_TRANSITIONS     = 'Выходящие переходы'


class StateBehaviorConsts():
    FORM                = 'Форма'
    INPUT_CHECK         = 'Проверка ввода'


class TransitionFieldConsts():
    NAME                = 'Название'
    SOURCE              = 'Откуда'
    TARGET              = 'Куда'
    FORM_CONDITIONS     = 'Эллемент формы'
    TRANSITION_CONDITION= 'Условие перехода'


class TransitionTypesConsts():
    CONDITIONAL         = 'По формам'
    STRICT              = 'Закончить все формы'
    UNCONDITIONAL       = 'Без условия'


class FormFieldConsts():
    NAME                = 'Название'
    TYPE                = 'Тип'
    STATE_ID            = 'Состояние'
    TAGS                = 'jinja tags'


class DocFieldConsts():
    NAME                = 'Иск'
    TAG                 = 'tag'
    DOC_NAME            = 'Название документа'

