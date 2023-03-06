from ..Storage      import UserStorageView 

from time           import time


def update_user_last_action_time(tg_user_id):
    try:
        UserStorageView(tg_user_id).Write('last_action_time', time())
        return True
    except:
        return False

