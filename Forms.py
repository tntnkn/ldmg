from Graph.Transition   import TransitionType


class FormElem():
    def __init__(self, transition, form):
        self.id     = transition["id"]
        self.form   = form
        self.text   = ''
        self.desc   = ''
        self.input  = ''
        self.completed      = False
        self.next_state_id  = transition['next_state_id']

        self.form.append(self)

    def IsCompleted(self) -> bool:
        pass

    def AcceptInput(input) -> bool:
        pass

    def GetNextState():
        pass


class RegularTextFormElem(FormElem):
    def __init__(self, transition, form):
        super().__init__(transition, form)
        self.completed = True


class RegularFieldFormElem(FormElem):
    def __init__(self, transition, form):
        super().__init__(transition, form)


class DynamicFieldFormElem(FormElem):
    def __init__(self, transition, form):
        super().__init__(transition, form)


class SingleChoiceFormElem(FormElem):
    def __init__(self, transition, form):
        super().__init__(transition, form)


class MultiChoiceFormElem(FormElem):
    def __init__(self, transition, form):
        super().__init__(transition, form)


class Form():
    def __init__(self, state, transitions):
        self.id             = state['id']
        self.fields         = dict()

        self.regular_texts  = list()
        self.regular_fields = list()
        self.dynamic_fields = list()
        self.single_choises = list()
        self.multi_choises  = list()
        self.documents      = list()

        for tr in transitions: 
            field = None
            match tr['type']:
                case TransitionType.REGULAR_TEXT:
                    field = RegularTextFormElem(tr, self.regular_texts)
                case TransitionType.REGULAR_FIELD:
                    field = RegularFieldFormElem(tr, self.regular_fields)
                case TransitionType.DYNAMIC_FIELD:
                    field = DynamicFieldFormElem(tr, self.dynamic_fields)
                case TransitionType.SINGLE_CHOICE:
                    field = SingleChoiceFormElem(tr, self.single_choises)
                case TransitionType.MULTI_CHOICE:
                    field = MultiChoiceFormElem(tr, self.multi_choises)
                case _:
                    raise 'Cannot make form, unsupported type!'
            self.fields[tr['id']] = field

    def IsCompleted(self) -> bool:
        pass

    def AcceptInput(input) -> bool:
        pass

    def GetNextState():
        pass


class State():
    def __init__(state, form, session_id):
        self.id     = state['id']
        self.form   = form
        self.session_id = session_id

    def IsCompleted(self) -> bool:
        pass

    def AcceptInput(input) -> bool:
        pass

    def GetNextState():
        pass


class FormPrototypeFactory():
    def __init__(self, states, transitions):
        self.prototypes     = dict()

        for state in states:
            if state['transitions_ids']:
                try:
                    self.prototypes[state['id']] = Form(
                        state,
                        [ transitions[tr_id] for 
                            tr_id in state['transitions_ids'] ]
                    )
                except:
                    pass

    def MakeForm(self, id):
        from copy import deepcopy
        return deepcopy(self.prototypes.get(id, None)) 


class StateHistory():
    def __init__(self):
        self.history    = list()

    def GetCurrentState(self):
        pass


class StateMachine():
    def __init__(self, graph):
        self.history    = StateHistory() 
        self.graph      = graph

    def go(self, input):
        # if input is 'next', then
        #   self.history.next or smth
        # if input is 'prev', then
        #   self.history.prev or smth
        # else:
        #   self.history.current().do_smth    
        pass
        


