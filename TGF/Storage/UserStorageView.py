from .  import Storage


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
        
