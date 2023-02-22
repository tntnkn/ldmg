from typing         import Dict, Union, List
from ..Static       import AllowedInputType
from ..Utils        import AllowedInputTypeHelper
from ..keyboards    import Form


class UserDataModel():
    back_id                 : Union[str, None]
    allowed_input_types     : int 
    form_desc               : Union[Dict, None]
    compressed_back_data    : Union[str, None]
    messages_displayed      : List
    displayed_form          : Union[Form, None]
    

class Storage():
    users = dict()

    def __init__(self):
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

