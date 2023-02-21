from typing import Dict, Union


class UserDataModel():
    back_id                 : Union[str, None]
    allowed_input           : Union[str, None]
    form_desc               : Union[Dict, None]
    compressed_back_data    : Union[str, None]
    


class Storage():
    users = dict()

    def __init__(self):
        pass

    def AddUser(self, tg_user_id):
        if self.HasUser(tg_user_id):
            self.DeleteUser(tg_user_id)
        Storage.users[tg_user_id] = {
            'back_id'                 : None,
            'allowed_input'           : None,
            'form_desc'               : None,
            'compressed_back_data'    : None,
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


class UserStorageView():
    def __init__(self, tg_user_id):
        s_h = Storage()
        if not s_h.HasUser(tg_user_id):
            s_h.AddUser(tg_user_id)
        self.data = s_h.GetUserData(tg_user_id)

    def Read(self, key):
        return self.data[key]

    def Write(self, key, value):
        self.data[key] = value
        
