from enum       import Enum, unique
from typing     import TypedDict, List, Dict, Union

from .Types     import ID_TYPE

@unique
class StateType(Enum):
    UNKNOWN             = 'UNKNOWN' 
    START               = 'START'
    END                 = 'END'
    ALWAYS_REACHABLE    = 'ALWAYS_REACHABLE'
    REGULAR             = 'REGULAR'


class State(TypedDict):
    id                              : ID_TYPE
    name                            : str
    type                            : StateType
    force_completion                : bool
    forms_ids                       : List[ID_TYPE]
    transitions_ids                 : List[ID_TYPE]
    is_start                        : bool
    is_end                          : bool
    is_always_reachable             : bool
    pin_widget                      : bool
    before_enter                    : List[str]
    before_leave                    : List[str]


def get_dummy_state() -> State:
    return {
        'id'                    : '',
        'name'                  : 'dummy',
        'type'                  : StateType.UNKNOWN,
        'force_completion'      : True,
        'forms_ids'             : list(),
        'transitions_ids'       : list(),
        'is_always_reachable'   : False,
        'is_start'              : False,
        'is_end'                : False,
        'pin_widget'            : False,
        'before_leave'          : list(),
        'before_enter'          : list()
    }


if __name__ == '__main__':
    state : State = get_dummy_state()
    print(state)

