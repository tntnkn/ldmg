from enum       import Enum, unique


@unique
class NodeType(Enum):
    UNKNOWN             = 'UNKNOWN' 
    START               = 'START'
    END                 = 'END'
    ALWAYS_REACHABLE    = 'ALWAYS_REACHABLE'
    REGULAR             = 'REGULAR'
    

@unique
class EdgeType(Enum):
    UNKNOWN             = 'UNKNOWN'
    CONDITIONAL         = 'CONDITIONAL'
    UNCONDITIONAL       = 'UNCONDITIONAL'
    ALWAYS_REACHABLE    = 'ALWAYS_REACHABLE'

