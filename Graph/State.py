from enum       import IntEnum, auto, unique
from typing     import TypedDict, List, Dict, Union


@unique
class StateType(IntEnum):
    UNKNOWN             = auto()
    START               = auto()
    ALWAYS_REACHABLE    = auto()
    REGULAR             = auto()


class State(TypedDict):
    id                              : int
    name                            : str
    graph_elem                      : Union[Dict, None] 
    type                            : StateType
    force_completion                : bool
    actions_ids                     : List[int] 
    is_start                        : bool
    is_always_reachable             : bool
    deletes_widget_history_force    : bool
    deletes_widget_before_switch    : bool
    deletes_widget_upon_session_end : bool


def get_dummy_state() -> State:
    return {
        'id'                    : 0,
        'name'                  : 'dummy',
        'graph_elem'            : None,
        'type'                  : StateType.UNKNOWN,
        'force_completion'      : True,
        'actions_ids'           : list(),
        'is_always_reachable'   : False,
        'is_start'              : False,
        'deletes_widget_history_force'    : False,
        'deletes_widget_before_switch'    : False,
        'deletes_widget_upon_session_end' : False,
    }


if __name__ == '__main__':
    state : State = get_dummy_state()
    print(state)

