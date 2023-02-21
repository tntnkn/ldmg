from ..API      import API
from .Messages  import *
from ..Exceptions   import UserDone
import uuid


class MonoAPI(API):
    def __init__(self, active_users, state_machine):
        super().__init__()
        self.active_users  = active_users
        self.state_machine = state_machine

    def NewUser(self) -> str:
        user_id = uuid.uuid4()
        self.active_users.AddUser(user_id)
        return user_id

    def AcceptInput(self, message: Message) -> Message:
        user_id = message['user_id']
        context = self.active_users.GetUserContext(user_id)
        try:
            form = self.state_machine.Go(context, 
                                         message['contents'])
            return {
                'user_id'   : user_id,
                'type'      : MessageType.FormOut,
                'contents'  : form,
            }
        except UserDone:
            info = context.user_input.ReadAll()
            return {
                'user_id'   : user_id,
                'type'      : MessageType.PositiveEnd,
                'contents'  : info,
            }
