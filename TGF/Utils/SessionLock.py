from ..Storage      import UserStorageView


class SessionLock():

    @staticmethod
    def Lock(tg_user_id):
        s_view = UserStorageView(tg_user_id)
        if s_view.Read('is_locked'):
            return False
        s_view.Write('is_locked', True)
        return True

    @staticmethod
    def Unlock(tg_user_id):
        UserStorageView(tg_user_id).Write('is_locked', False)
        return True

