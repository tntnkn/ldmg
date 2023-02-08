from copy   import deepcopy

from .                  import Models as M
from .StorageInterface  import StorageInterface
from .Context           import Context, UserInputStorage, UserContextStorage, GeneralInfoStorage


class Storage(StorageInterface):
    def __init__(self, 
                 user_input_model: M.UserInput, 
                 general_info: M.GeneralInfo):
        self.user_input_model: M.UserInputModel = user_input_model
        self.general_info: M.GeneralInfo = general_info
        self.main_storage: M.MainStorage = dict() 

    def HasUser(self, user_id):
        if user_id in self.main_storage:
            return True
        return False

    def AssertUser(self, user_id):
        if not self.HasUser(user_id):
            raise 'User is not in the database!'

    def AddUser(self, user_id):
        if self.HasUser(user_id):
            raise 'User already added!'
        new_user_info : M.MainStorageContents = {
            'user_context'    : {
                'current_state_idx' : 0,
                'state_history'     : [self.general_info['start_id'],],
            },
            'user_input'      : deepcopy(self.user_input_model),
        }
        self.__NewUser(user_id, new_user_info)

    def GetUserContext(self, user_id):
        return Context( self.__GetUserInput(user_id),
                        self.__GetUserContext(user_id),
                        self.__GetGeneralInfoStorage() )

    def __GetUserInput(self, user_id):
        self.AssertUser(user_id)
        return UserInputStorage( 
            self.main_storage[user_id]['user_input'] )

    def __GetUserContext(self, user_id):
        self.AssertUser(user_id)
        return UserContextStorage(  
            self.main_storage[user_id]['user_context'] )

    def __GetGeneralInfoStorage(self):
        return GeneralInfoStorage(self.general_info)

    def __NewUser(self, user_id, new_user_info):
        self.main_storage[user_id] = new_user_info

