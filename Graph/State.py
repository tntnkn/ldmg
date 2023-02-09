from typing     import TypedDict, List, Dict, Union
from enum       import Enum, unique

from .Types     import ID_TYPE


@unique
class StateType(Enum):
    UNKNOWN             = 'UNKNOWN' 
    START               = 'START'
    END                 = 'END'
    REGULAR             = 'REGULAR'
    ALWAYS_OPEN         = 'ALWAYS_OPEN'


class State(TypedDict):
    id                              : ID_TYPE
    name                            : str
    type                            : StateType
    is_start                        : bool
    is_end                          : bool
    forms_ids                       : List[ID_TYPE]
    in_transitions_ids              : List[ID_TYPE]
    out_transitions_ids             : List[ID_TYPE]


def get_dummy_state() -> State:
    return {
        'id'                    : '',
        'name'                  : 'dummy',
        'type'                  : StateType.UNKNOWN,
        'is_start'              : False,
        'is_end'                : False,
        'forms_ids'             : list(),
        'in_transitions_ids'    : list(),
        'out_transitions_ids'   : list(),
    }


if __name__ == '__main__':
    state : State = get_dummy_state()
    print(state)

