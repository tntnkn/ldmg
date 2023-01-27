from enum       import Enum, unique
from typing     import TypedDict, List, Dict, Union

from .Types     import ID_TYPE

@unique
class TransitionType(Enum):
    UNKNOWN         = 'UNKNOWN'
    CONDITIONAL     = 'CONDITIONAL'
    UNCONDITIONAL   = 'UNCONDITIONAL'
    ALWAYS_REACHABLE= 'ALWAYS_REACHABLE'


@unique
class OperatorType(Enum):
    NONE        = 'NONE'
    EQUALS      = 'EQUALS'


class Transition(TypedDict, total=True):
    id              : ID_TYPE
    name            : str
    type            : TransitionType
    source_id       : ID_TYPE
    target_id       : ID_TYPE
    form_elem_id    : ID_TYPE
    cond_operator   : OperatorType
    cond_value      : str


def get_always_reachable_transition(id : ID_TYPE, 
                                    source_id : ID_TYPE,
                                    target_id : ID_TYPE) ->\
        Transition:
    return {
        'id'            : id,
        'name'          : TransitionType.ALWAYS_REACHABLE.value,
        'type'          : TransitionType.ALWAYS_REACHABLE,
        'source_id'     : source_id,
        'target_id'     : target_id,
        'form_elem_id'  : '',
        'cond_operator' : OperatorType.NONE,
        'cond_value'    : '',
    }


def get_dummy_transition() -> Transition:
    return {
        'id'            : '',
        'name'          : 'dummy',
        'type'          : TransitionType.UNKNOWN,
        'source_id'     : '',
        'target_id'     : '',
        'form_elem_id'  : '',
        'cond_operator' : OperatorType.NONE,
        'cond_value'    : '',
    }

if __name__ == '__main__':
    transition : Transition = get_dummy_transition()
    print(transition)

