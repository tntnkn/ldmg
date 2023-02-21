from aiogram.types              import Message, CallbackQuery
from aiogram.dispatcher.filters import BoundFilter
from aiogram.types              import Message

import services.sessionManager  as sessionManager
import states.general           as statesGeneral


sm = sessionManager.get()


class isPromtingForUserInfo(BoundFilter):
    async def check(self, message: Message):
        if not sm.hasSession(message.from_id):
            return False
        if not isinstance(sm.getSession(message.from_id).current_state,
                          statesGeneral.gettingUserInfo):
            return False
        return True

class isFillingUserInfoForm(BoundFilter):
    async def check(self, callback_query: CallbackQuery):
        from_id = callback_query["from"]["id"]
        if not sm.hasSession(from_id):
            return False
        if not isinstance(sm.getSession(from_id).current_state,
                          statesGeneral.gettingUserInfoFormInput):
            return False
        return True

class isSelectingUserConditionsOptions(BoundFilter):
    async def check(self, callback_query: CallbackQuery):
        from_id = callback_query["from"]["id"]
        if not sm.hasSession(from_id):
            return False
        if not isinstance(sm.getSession(from_id).current_state,
                          statesGeneral.gettingUserCondition):
            return False
        return True

