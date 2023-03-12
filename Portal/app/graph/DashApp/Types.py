from enum       import Enum, unique


@unique
class NodeType(Enum):
    UNKNOWN             = 'UNKNOWN' 
    START               = 'START'
    END                 = 'END'
    REGULAR             = 'REGULAR'
    ALWAYS_OPEN         = 'ALWAYS_OPEN'
    

@unique
class EdgeType(Enum):
    UNKNOWN             = 'UNKNOWN'
    CONDITIONAL         = 'CONDITIONAL'
    UNCONDITIONAL       = 'UNCONDITIONAL'
    STRICT              = 'STRICT'
    ALWAYS_REACHABLE    = 'ALWAYS_REACHABLE'

