from enum       import IntEnum, auto, unique


@unique
class AllowedInputType(IntEnum):
    COMMAND     = 1
    CB          = 2
    TEXT        = 4
    COMMANDS    = 8

