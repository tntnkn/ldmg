from enum       import IntEnum, auto, unique
from typing     import TypedDict, List, Dict, Union


@unique
class StateType(IntEnum):
    UNKNOWN             = auto()
    START               = auto()
    END                 = auto()
    ALWAYS_REACHABLE    = auto()
    REGULAR             = auto()


class State(TypedDict):
    id                              : int
    name                            : str
    graph_elem                      : Union[Dict, None] 
    type                            : StateType
    force_completion                : bool
    transitions_ids                 : List[int] 
    is_start                        : bool
    is_end                          : bool
    is_always_reachable             : bool
    pin_widget                      : bool
    before_enter                    : List[str]
    before_leave                    : List[str]


def get_dummy_state() -> State:
    return {
        'id'                    : 0,
        'name'                  : 'dummy',
        'graph_elem'            : None,
        'type'                  : StateType.UNKNOWN,
        'force_completion'      : True,
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

