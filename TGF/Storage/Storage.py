from typing         import Dict, Union, List, TypedDict

from ..Static       import AllowedInputType
from ..Utils        import AllowedInputTypeHelper
from ..keyboards    import Form


class BackInfo(TypedDict):
    start_id        : str 
    end_ids         : List[str]
    always_open_ids : List[str]
    states_names    : List[str]


class Command(TypedDict):
    command         : str 
    description     : str 
    back_id         : str


class CommandsInfo(TypedDict):
    commands        : List[Command]


class UserDataModel():
    back_id                 : Union[str, None]
    allowed_input_types     : int 
    form_desc               : Union[Dict, None]
    compressed_back_data    : Union[str, None]
    messages_displayed      : List
    displayed_form          : Union[Form, None]


class Storage():
    users       : UserDataModel             = dict()
    back_info   : Union[BackInfo, None]     = None 
    commands    : Union[List[str], None]    = None

    def __init__(self):
        #returns a handle
        pass

    def AddUser(self, tg_user_id):
        if self.HasUser(tg_user_id):
            self.DeleteUser(tg_user_id)

        allowed_input_types = \
            AllowedInputTypeHelper.SetAllowedInputTypes(
                    AllowedInputType.COMMAND)
        Storage.users[tg_user_id] = {
            'back_id'                 : None,
            'allowed_input_types'     : allowed_input_types,
            'form_desc'               : None,
            'compressed_back_data'    : None,
            'messages_displayed'      : list(),
            'displayed_form'          : None,
        }

    def DeleteUser(self, tg_user_id):
        if not self.HasUser(tg_user_id):
            return
        Storage.users.pop(tg_user_id)

    def HasUser(self, tg_user_id):
        return Storage.users.get(tg_user_id, None) != None

    def GetUserData(self, tg_user_id):
        if not self.HasUser(tg_user_id):
            raise 'No user with tg id ' + str(tg_user_id)
        return Storage.users[tg_user_id]

    def SetBackInfo(self, back_info):
        Storage.back_info = back_info

    def GetBackInfo(self):
        return Storage.back_info

    def SetCommands(self, commands):
        Storage.commands = commands

    def GetCommands(self):
        return Storage.commands

