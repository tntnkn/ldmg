from ..Storage  import ActiveUsers

class ActiveUsersFactory():

    storage = None
    def INIT(storage):
        ActiveUsersFactory.storage = storage

    def Make():
        return ActiveUsers(ActiveUsersFactory.storage)

