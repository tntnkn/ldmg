from typing      import Dict
from .State      import State, StateType
from .Transition import Transition, TransitionType


def get_node_type_class(state: State) -> str:
    match state['type']:
        case StateType.START:
            return 'start_node '
        case StateType.END:
            return 'end_node '
        case StateType.ALWAYS_REACHABLE:
            return 'always_reachable_node '
        case StateType.REGULAR:
            return 'regular_node '
        case _:
            return ''


def get_edge_type_class(transition : Transition) -> str:
    match transition['type']:
        case TransitionType.REGULAR_TEXT:
            return 'regular_text ' 
        case TransitionType.REGULAR_FIELD:
            return 'regular_field ' 
        case TransitionType.DYNAMIC_FIELD:
            return 'dynamic_field ' 
        case TransitionType.SINGLE_CHOICE:
            return 'single_choice ' 
        case TransitionType.MULTI_CHOICE:
            return 'multi_choice ' 
        case TransitionType.DOCUMENT:
            return 'document ' 
        case TransitionType.DEFAULT:
            return 'default ' 
        case TransitionType.ALWAYS_REACHABLE:
            return 'always_reachable ' 
        case _:
            return ''

