from .  import Storage


class UserStorageView():
    def __init__(self, tg_user_id):
        s_h = Storage()
        if not s_h.HasUser(tg_user_id):
            raise RuntimeError(f"No registered user with id {tg_user_id}")
        self.data = s_h.GetUserData(tg_user_id)
        self.tg_user_id = tg_user_id

    def Destroy(self):
        s_h = Storage()
        s_h.DeleteUser(self.tg_user_id)
        self.data = None
        self.tg_user_id = None

    def Read(self, key):
        return self.data[key]

    def Write(self, key, value):
        self.data[key] = value

    def GetUserId(self):
        return self.tg_user_id
        
