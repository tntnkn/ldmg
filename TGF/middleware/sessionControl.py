from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.dispatcher.handler     import CancelHandler
from aiogram import types

from services.sessionManager import sessionManager
from static.types            import userSession 

sm = sessionManager.get()

class sessionControl(BaseMiddleware):
    async def on_process_update(self, update: types.Update, data: dict):
        #print("IN SESSION CONTROL")
        if   "message" in update:
            self.__on_process_update_message(update, data)
        elif "callback_query" in update:
            self.__on_process_update_callback_query(update, data)
        else:
            raise CancelHandler()
        if not sm.lockSession(data["session"].from_id):
            raise CancelHandler()

    def __on_process_update_message(self, update, data: dict):
        message = update["message"]
        from_id = message["from"]["id"]
        if not sm.hasSession(from_id):
            sm.addSession(from_id)
        session = sm.getSession(from_id)  
        sm.recordSessionAction(from_id)
        session.from_id = from_id
        session.message = message 
        session.ms_text = message["text"] 
        data["session"] = session

    def __on_process_update_callback_query(
            self, update: types.Update, data: dict):
        cb_query= update["callback_query"]
        from_id = cb_query["from"]["id"] 
        if not sm.hasSession(from_id):
            sm.addSession(from_id)
        session = sm.getSession(from_id)  
        sm.recordSessionAction(from_id)
        session.from_id = from_id
        session.message = cb_query.message 
        session.ms_text = session.message["text"] 
        session.cb_query= cb_query
        session.cb_data = cb_query["data"]
        data["session"] = session

    async def on_post_process_update(
            self, update: types.Update,data_from_handler: list, data: dict):
        session = data["session"]
        sm.unlockSession(session.from_id)
        if session.current_state is None:
            await sm.deleteSession(session.from_id)
        
