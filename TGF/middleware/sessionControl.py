from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.dispatcher.handler     import CancelHandler
from aiogram import types

from ..Utils                        import (SessionLock, 
                                            update_user_last_action_time)
from ..Storage                      import Storage


class sessionControl(BaseMiddleware):
    async def on_process_update(
            self, 
            update: types.Update, 
            data: dict):
        print('IN ON PRE PROCESS')
        tg_user_id = sessionControl.__get_tg_id(update)
        if not tg_user_id:
            raise CancelHandler()

        print('BEFIRE STORAGE')
        s_h = Storage()
        if not s_h.HasUser(tg_user_id):
            s_h.AddUser(tg_user_id)
        
        if not SessionLock.Lock(tg_user_id):
            raise CancelHandler()
        print('SESSION LOCKED')

        update_user_last_action_time(tg_user_id)
        print('TIME UPDATED')

    async def on_post_process_update(
            self, 
            update: types.Update,
            data_from_handler: list,
            data: dict):
        print('IN ON POST PROCESS')
        tg_user_id = sessionControl.__get_tg_id(update)
        if not tg_user_id:
            raise CancelHandler()

        try:
            SessionLock.Unlock(tg_user_id)
        except:
            print('SOME SHIT HAPPENED')
            pass
        
    def __get_tg_id(update):
        tg_user_id = None
        if   "message" in update:
            tg_user_id = update['message']['from']['id']
        elif "callback_query" in update:
            tg_user_id = update['callback_query']['from']['id']
        return tg_user_id

