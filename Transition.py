from enum       import Enum, auto, unique
from typing     import TypedDict, List, Dict, Union


@unique
class TransitionType(Enum):
    UNKNOWN         = 'UNKNOWN TYPE!'
    REGULAR_TEXT    = 'Простой текст'
    REGULAR_FIELD   = 'Поле для заполнения'
    DYNAMIC_FIELD   = 'Поле для заполнения динамическое'
    SINGLE_CHOICE   = 'Кнопка единичного выбора'
    MULTI_CHOICE    = 'Кнопка множественного выбора'
    DOCUMENT        = 'Документ'
    DEFAULT         = 'По умолчанию' 
    ALWAYS_REACHABLE= 'Всегда доступно'


class Transition(TypedDict, total=True):
    id              : int
    name            : str
    graph_elem      : Union[Dict, None] 
    type            : TransitionType
    property_name   : Union[str, None]
    value           : Union[str, None]
    next_state_id   : Union[int, None]


def get_always_reachable_transition(id : int, next_state_id : int) ->\
        Transition:
    return {
        'id'            : id,
        'name'          : TransitionType.ALWAYS_REACHABLE.value,
        'graph_elem'    : None,
        'type'          : TransitionType.ALWAYS_REACHABLE,
        'property_name' : None,
        'value'         : None,
        'next_state_id' : next_state_id,
    }


def get_dummy_transition() -> Transition:
    return {
        'id'            : 0,
        'name'          : 'dummy',
        'graph_elem'    : None,
        'type'          : TransitionType.UNKNOWN,
        'property_name' : None,
        'value'         : None,
        'next_state_id' : 0,
    }

if __name__ == '__main__':
    transition : Transition = get_dummy_transition()
    print(transition)

