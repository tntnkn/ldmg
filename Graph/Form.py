from enum       import Enum, auto, unique
from typing     import TypedDict, List, Dict, Union

from .Types     import ID_TYPE


@unique
class FormType(Enum):
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


class Form(TypedDict, total=True):
    id              : ID_TYPE
    name            : str
    type            : FormType
    value           : Union[str, None]


def get_dummy_form() -> Form:
    return {
        'id'            : '0',
        'name'          : 'dummy',
        'type'          : FormType.UNKNOWN,
        'value'         : None,
    }

if __name__ == '__main__':
    form : Form = get_dummy_form()
    print(form)

