from collections    import OrderedDict

from .Factories     import FormElemFactory
from .Interface     import FormElem
from .StateHistory  import StateHistory
from .Exceptions    import FormElemSwitchedHistory


class Form():
    def __init__(self, form_id, fields):
        self.id             = form_id 
        self.fields         = OrderedDict()

        self.can_go_next    = False
        self.can_go_prev    = False
        self.can_be_done    = False

        self.next_b_tpl     = {
            'id'        : 'next',
            'type'      : 'BUTTON',
            'cb'        : 'next',
            'text'      : 'ДАЛЕЕ',
        }
        self.prev_b_tpl     = {
            'id'        : 'prev',
            'type'      : 'BUTTON',
            'cb'        : 'prev',
            'text'      : 'НАЗАД',
        }
        self.done_b_tpl     = {
            'id'        : 'done',
            'type'      : 'BUTTON',
            'cb'        : 'done',
            'text'      : 'ВСЁ',
        }

        for f in fields: 
            self.fields[f['id']] = FormElemFactory.Make(f)

    def IsCompleted(self, context):
        for field in self.form:
            if not field.IsCompleted(context):
                return False
        return True

    def IsFieldCompleted(self, field_id):
        return self.fields[field_id].IsCompleted()

    def AcceptInput(self, input, context):
        field = self.fields[input['field_id']]
        try:
            field.AcceptInput(input, context)
        except FormElemSwitchedHistory:
            return
        next_id = StateHistory.DetermineNextState(context)
        StateHistory.SetNext(next_id, context)

    def Reject(self, context):
        for field in self.fields.values():
            field.Reject(context)

    def ToDict(self, context):
        repr = list()
        for field in self.fields.values():
            field.AddRepr(repr, context)
        if   StateHistory.CanSwitchToPrev(context):
            repr.append(self.prev_b_tpl)
        if   StateHistory.CanSwitchToNext(context):
            repr.append(self.next_b_tpl)
        elif StateHistory.AtEnd(context):
            repr.append(self.done_b_tpl)
        return repr

    def ToJson(self):
        return json.dumps( self.ToDict() )

