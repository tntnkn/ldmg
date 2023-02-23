from typing     import Dict
from .Types     import NodeType, EdgeType


def get_node_type_class(node_type : str) -> str:
    print("-- NODE TYPE IS ", node_type)
    match node_type:
        case NodeType.START.value:
            return 'start_node '
        case NodeType.END.value:
            return 'end_node '
        case NodeType.ALWAYS_OPEN.value:
            return 'always_reachable_node '
        case NodeType.REGULAR.value:
            return 'regular_node '
        case _:
            return ''


def get_edge_type_class(edge_type : str) -> str:
    print("-- EDGE TYPE IS ", edge_type)
    match edge_type:
        case EdgeType.CONDITIONAL.value:
            return 'cond_edge ' 
        case EdgeType.UNCONDITIONAL.value:
            return 'uncond_edge ' 
        case EdgeType.STRICT.value:
            return 'strict_edge ' 
        case EdgeType.ALWAYS_REACHABLE.value:
            return 'always_reachable_edge ' 
        case _:
            return ''

