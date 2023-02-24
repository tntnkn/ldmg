from ..Storage  import Models as M
from typing     import TypedDict, Dict, Union


class MessageType():
    Input       = 'input'
    FormOut     = 'form'
    DocInfoOut  = 'doc_info'


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


class OutForm(TypedDict):
    form        : Form


Tag = str 
Inp = str
class OutInfoForDocgen(TypedDict):
    tags        : Dict[Tag, Inp]
    docs        : M.Documents


class Message(TypedDict):
    user_id     : M.ID 
    type        : str
    contents    : Union[Input, OutForm, OutInfoForDocgen, None]

