from ..Storage  import Models as M
from typing     import TypedDict, Dict, Union


Form = Dict


class Input(TypedDict):
    field_type  : str
    field_id    : M.ID
    cb          : str


class Output(TypedDict):
    form        : Form


class Message(TypedDict):
    user_id     : M.ID 
    type        : str
    contents    : Union[Input, Output, None]


class MessageType():
    Input       = 'input'
    FormOut     = 'form'
    PositiveEnd = 'pos_end'

