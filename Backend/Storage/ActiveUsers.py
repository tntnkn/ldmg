from .StorageInterface  import StorageInterface
from .Models            import UserContext


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

