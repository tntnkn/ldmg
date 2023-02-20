from .StateHistory  import StateHistory
from .Factories     import FormPrototypeFactory
from .Exceptions    import UserDone


class StateMachine():
    def __init__(self):
        pass

    def Go(self, context, input=None):
        self.Process(context, input)
        cur_id = StateHistory.GetCurrent(context)
        form = FormPrototypeFactory.Get(cur_id)
        return form.ToDict(context)

    def Process(self, context, input):
        if input is None:
            pass
        elif input['field_id'] == 'next':
            StateHistory.SwitchToNext(context)
        elif input['field_id'] == 'prev':
            StateHistory.SwitchToPrev(context)
        elif input['field_id'] == 'done':
            print("WE ARE DONE!")
            raise UserDone
        else:
            cur_id = StateHistory.GetCurrent(context)
            form = FormPrototypeFactory.Get(cur_id)
            form.AcceptInput(input, context)

