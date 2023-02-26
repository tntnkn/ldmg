import uuid

from ..API          import API
from .Messages      import *
from ..Exceptions   import UserDone


class MonoAPI(API):
    def __init__(self, active_users, general_info, state_machine):
        super().__init__()
        self.active_users  = active_users
        self.state_machine = state_machine
        self.general_info  = general_info

    def RegisterFrontendAPI(self, api):
        contents = {
            'start_id'        : self.general_info.Read('start_id'),
            'end_ids'         : self.general_info.Read('end_ids'),
            'always_open_ids' : self.general_info.Read('always_open_ids'),
            'states_names'    : self.general_info.Read('forms_names'),
        }
        return {
            'user_id'   : None,
            'type'      : MessageType.FrontAccepted,
            'contents'  : contents,
        }

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
            tags = context.general_info.Read('tags_by_field_id')
            inps = context.user_input.ReadAll()

            tags_inps = dict()
            for f_id, tgs in tags.items():
                if not tgs:
                    continue
                for t in tgs.split(','):
                    tags_inps[t] = inps[f_id]

            contents = {
                'tags'      : tags_inps,
            }

            return {
                'user_id'   : user_id,
                'type'      : MessageType.DocInfoOut,
                'contents'  : contents,
            }

