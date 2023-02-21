from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram import types



class testMiddleware(BaseMiddleware):
    async def on_pre_process_update(self, update: types.Update, data: dict):
        #print("ON PRE PROCESS UPDATE", update, data, "\n")
        pass

    async def on_process_update(self, update: types.Update, data: dict):
        print("ON PROCESS UPDATE", update, data, "\n")
        pass

    async def on_pre_process_message(
            self, update: types.Message, data: dict):
        #print("ON PRE PROCESS MESSAGE", update, data, "\n")
        pass

    async def on_filters(self, mes: types.Message, data: dict):
        #print("ON FILTERS", update, data, "\n")
        pass

    async def on_post_process_update(
            self, update: types.Update, data_from_handler, data):
        #print("ON POST PROCESS UPDATE", update, data, "\n")
        pass
