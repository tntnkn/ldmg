from ..Storage      import UserStorageView
from .              import MessageManager


class MessagesArchive():
    @staticmethod
    def Memo(message_id, tg_user_id):
        s_view = UserStorageView(tg_user_id)
        messages = s_view.Read('messages_displayed')
        messages.append(message_id)
        s_view.Write('messages_displayed', messages)

    async def Clear(tg_user_id):
        s_view = UserStorageView(tg_user_id)
        messages = s_view.Read('messages_displayed')
        for mess_id in messages:
            await MessageManager.Delete(mess_id, tg_user_id)
        messages = list()
        s_view.Write('messages_displayed', messages)

