from collections    import OrderedDict

from .Factories     import FormElemFactory
from .Interface     import FormElem
from .StateHistory  import StateHistory
from .Exceptions    import FormElemSwitchedHistory
from .Storage       import Context, Models as M
from typing         import Dict, List
import json


class Form():
    def __init__(self, form_id: M.ID, fields):
        self.id             = form_id 
        self.fields         = OrderedDict()

        for f in fields: 
            self.fields[f['id']] = FormElemFactory.Make(f)

        self.next_b_tpl     = {
            'id'        : 'next',
            'type'      : 'BUTTON',
            'cb'        : 'next',
            'text'      : 'ДАЛЕЕ',
            'completed' : False,
        }
        self.prev_b_tpl     = {
            'id'        : 'prev',
            'type'      : 'BUTTON',
            'cb'        : 'prev',
            'text'      : 'НАЗАД',
            'completed' : False,
        }
        self.done_b_tpl     = {
            'id'        : 'done',
            'type'      : 'BUTTON',
            'cb'        : 'done',
            'text'      : 'ВСЁ',
            'completed' : False,
        }

    def IsCompleted(self, context: Context) -> bool:
        for field in self.fields:
            if not field.IsCompleted(context):
                return False
        return True

    def IsFieldCompleted(self, field_id: M.ID) -> bool:
        return self.fields[field_id].IsCompleted()

    def AcceptInput(self, input, context: Context) -> None:
        field = self.fields[input['field_id']]
        try:
            field.AcceptInput(input, context)
        except FormElemSwitchedHistory:
            return
        next_id = StateHistory.DetermineNextState(context)
        StateHistory.SetNext(next_id, context)

    def Reject(self, context: Context) -> None:
        for field in self.fields.values():
            field.Reject(context)

    def ToDict(self, context: Context) -> List[Dict]:
        repr: List[Dict] = list()
        for field in self.fields.values():
            field.AddRepr(repr, context)
        if   StateHistory.CanSwitchToPrev(context):
            repr.append(self.prev_b_tpl)
        if   StateHistory.CanSwitchToNext(context):
            repr.append(self.next_b_tpl)
        elif StateHistory.AtEnd(context):
            repr.append(self.done_b_tpl)
        return repr

    def ToJson(self, context) -> str:
        return json.dumps( self.ToDict(context) )

