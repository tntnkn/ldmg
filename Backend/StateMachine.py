from .StateHistory  import StateHistory
from .Factories     import FormPrototypeFactory
from .Exceptions    import UserDone


class StateMachine():
    def __init__(self):
        pass

    def Go(self, context, input=None):
        self.__Process(context, input)
        self.__HandleRejectedStates(context)
        cur_id = StateHistory.GetCurrent(context)
        form = FormPrototypeFactory.Get(cur_id)
        return form.ToDict(context)

    def __Process(self, context, input):
        if input is None:
            pass
        elif input['field_id'] == 'next':
            StateHistory.SwitchToNext(context)
        elif input['field_id'] == 'prev':
            StateHistory.SwitchToPrev(context)
        elif input['field_id'] == 'done':
            print("WE ARE DONE!")
            raise UserDone
        elif input['field_id'] == 'done':
            print("WE ARE DONE!")
            raise UserDone
        elif input['field_id'] is None:
            # this one is for always reachable states
            next_id = input['cb']
            cur_id  = StateHistory.GetCurrent(context)
            if next_id == cur_id:
                return
            StateHistory.SetNext(next_id, context) 
            StateHistory.SwitchToNext(context)
        else:
            cur_id = StateHistory.GetCurrent(context)
            form = FormPrototypeFactory.Get(cur_id)
            form.AcceptInput(input, context)

    def __HandleRejectedStates(self, context):
        rejected = context.user_context.Read('rejected_states')
        while len(rejected) != 0:
            r = rejected.pop()
            form = FormPrototypeFactory.Get(r)
            form.Reject(context)
        context.user_context.Write('rejected_states', rejected)

