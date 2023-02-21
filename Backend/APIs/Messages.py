from ..Storage  import Models as M
from typing     import TypedDict, Dict, Union


class MessageType():
    Input       = 'input'
    FormOut     = 'form'
    PositiveEnd = 'pos_end'


class Form(TypedDict):
    id        : M.ID
    type      : MessageType
    cb        : str 
    text      : str
    completed : bool


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

