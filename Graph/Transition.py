from typing     import TypedDict, List, Dict, Union
from enum       import Enum, unique

from .Types     import ID_TYPE


@unique
class TransitionType(Enum):
    UNKNOWN         = 'UNKNOWN'
    CONDITIONAL     = 'CONDITIONAL'
    UNCONDITIONAL   = 'UNCONDITIONAL'


class Transition(TypedDict, total=True):
    id              : ID_TYPE
    name            : str
    type            : TransitionType
    source_id       : ID_TYPE
    target_id       : ID_TYPE
    form_elem_ids   : List[ID_TYPE]

"""
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
        'form_elem_ids' : '',
    }
"""

def get_dummy_transition() -> Transition:
    return {
        'id'            : '',
        'name'          : 'dummy',
        'type'          : TransitionType.UNKNOWN,
        'source_id'     : '',
        'target_id'     : '',
        'form_elem_ids' : list(),
    }

if __name__ == '__main__':
    transition : Transition = get_dummy_transition()
    print(transition)

