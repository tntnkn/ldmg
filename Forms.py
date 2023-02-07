from typing     import TypedDict, Dict, List, Union

ID = str

UserInput = Dict[ID, Union[str, None]]

class UserContext(TypedDict):
    current_state_id    : ID 
    next_state_idx      : int
    state_history       : List[ID]

class Branch(TypedDict):
    req_user_input_ids  : List[ID] 
    resulting_state_id  : ID

StateBranches = List[Branch]

StatesBranchesStorage = Dict[ID, StateBranches]

class MainStorageContents(TypedDict):
    user_context        : UserContext
    user_input          : UserInput

MainStorage = Dict[ID, MainStorageContents]

class GeneralInfo(TypedDict):
    brahches            : StatesBranchesStorage
    start_id            : ID


class StorageFactory():
    graph = None
    forms = None

    def INIT(graph, forms):
        StorageFactory.graph = graph
        StorageFactory.forms = forms

    def Make():
        g = StorageFactory.graph
        user_input_model : UserInput = {
            field['id']: None for field in
                StorageFactory.forms.values() }
        states_branches_storage : StatesBranchesStorage = dict()
        for s_id, state in g.states.items():
            branches : StateBranches = list()
            for tr_id in state['transitions_ids']:
                branch : Brach = {
                    'req_user_input_ids' : 
                        g.transitions[tr_id]['form_elem_id'],
                    'resulting_state_id' :
                        g.transitions[tr_id]['target_id'],
                }
                branches.append(branch)
            states_branches_storage[s_id] = branches
        general_info : GeneralInfo = {
            'branches' : states_branches_storage,
            'start_id' : g.start_node_id,
        }
        return Storage(user_input_model, general_info)


class ActiveUsersFactory():
    storage = None
    def INIT(storage):
        ActiveUsersFactory.storage = storage

    def Make():
        return ActiveUsers(ActiveUsersFactory.storage)


from copy   import deepcopy

class StorageInterface():
    def __init__(self)                  : pass
    def HasUser(self, user_id)          : pass
    def AssertUser(self, user_id)       : pass
    def AddUser(self, user_id)          : pass
    def GetUserContext(self, user_id)   : pass

class Storage(StorageInterface):
    def __init__(self, 
                 user_input_model: UserInput, 
                 general_info: GeneralInfo):
        self.user_input_model: UserInputModel = user_input_model
        self.general_info: GeneralInfo = general_info
        self.main_storage: MainStorage = dict() 

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
        new_user_info : MainStorageContents = {
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

class StorageView():
    def __init__(self, storage_part):
        self.storage = storage_part 

    def Read(self, key):
        return self.storage[key]

    def Write(self, key, value):
        self.storage[key] = value

    def Delete(self, key):
        self.storage[key] = None

    def Contains(self, key):
        return self.storage.get(key, None) is not None

    def TransactionGo(self):
        pass

class UserInputStorage(StorageView):
    def __init__(self, user_storage ):
        super().__init__(user_storage)


class UserContextStorage(StorageView):
    def __init__(self, user_context):
        super().__init__(user_context)


class GeneralInfoStorage(StorageView):
    def __init__(self, general_info):
        super().__init__(general_info)

    def Write(self, key, value):
        raise 'Operation "Write" is not supported!'

    def Delete(self, key):
        raise 'Operation "Delete" is not supported!'

class Context():
    def __init__(self, user_input, user_context, general_info):
        self.user_input     = user_input
        self.user_context   = user_context
        self.general_info   = general_info


class ActiveUsers(StorageInterface):
    def __init__(self, storage):
        self.storage : StorageInterface = storage
        self.user_context_cache : Dict[ID, UserContext] = dict()

    def HasUser(self, user_id): 
        self.storage.HasUser(user_id)

    def AssertUser(self, user_id): 
        self.storage.AssertUser(user_id)

    def AddUser(self, user_id): 
        self.storage.AddUser(user_id)

    def GetUserContext(self, user_id): 
        if user_id not in self.user_context_cache:
            self.user_context_cache[user_id] =\
                self.storage.GetUserContext(user_id)
        return self.user_context_cache[user_id]

