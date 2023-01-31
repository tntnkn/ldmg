from typing             import Dict
from Types              import FormType
import json


class FormElem():
    def __init__(self, field, form):
        self.id     = field['id']
        self.field  = field
        self.form   = form
        self.text   = field['name'] 
        self.desc   = ''
        self.cb     = field['id']
        self.completed  = False
        self.storage_id = field['id']

        self.form.append(self)

    def IsCompleted(self) -> bool:
        return self.completed

    def AcceptInput(self, input, storage) -> bool:
        storage.Write(self.storage_id, input['field_id'])
        print('Was Written', self.storage_id, storage.Contains(self.storage_id))

    def Reject(self, storage):
        storage.Delete(self.storage_id)

    def ToDict(self) -> Dict:
        return {
            'id'    : self.id,
            'type'  : self.type,
            'cb'    : self.cb,
            'text'  : self.text,
        }
    def ToJson(self) -> str:
        return json.dumps( self.ToDict() )


class RegularTextFormElem(FormElem):
    def __init__(self, field, form):
        super().__init__(field, form)
        self.completed  = True
        self.type       = 'TEXT'


class RegularFieldFormElem(FormElem):
    def __init__(self, field, form):
        super().__init__(field, form)
        self.type       = 'FORM'


class DynamicFieldFormElem(FormElem):
    def __init__(self, field, form):
        super().__init__(field, form)
        self.type       = 'D_FORM'


class ButtonFormElem(FormElem):
    def __init__(self, field, form):
        super().__init__(field, form)
        self.type       = 'BUTTON'


class SingleChoiceFormElem(FormElem):
    def __init__(self, field, form):
        super().__init__(field, form)
        self.type       = 'S_CHOICE'


class MultiChoiceFormElem(FormElem):
    def __init__(self, field, form):
        super().__init__(field, form)
        self.type       = 'M_CHOICE'


class DocumentFormElem(FormElem):
    def __init__(self, field, form):
        super().__init__(field, form)
        self.type       = 'DOCUMENT'


from collections import OrderedDict
class Form():
    def __init__(self, state, fields):
        self.id             = state['id']
        self.fields         = OrderedDict()
        self.changed_fields = list()

        self.regular_texts  = list()
        self.regular_fields = list()
        self.dynamic_fields = list()
        self.single_choises = list()
        self.multi_choises  = list()
        self.buttons        = list()
        self.documents      = list()

        self.can_go_next    = False
        self.can_go_prev    = False
        self.can_be_done    = False

        self.next_b_tpl     = {
            'id'        : 'NEXT',
            'type'      : 'BUTTON',
            'cb'        : 'next',
            'text'      : 'ДАЛЕЕ',
        }
        self.prev_b_tpl     = {
            'id'        : 'PREV',
            'type'      : 'BUTTON',
            'cb'        : 'prev',
            'text'      : 'НАЗАД',
        }
        self.done_b_tpl     = {
            'id'        : 'DONE',
            'type'      : 'BUTTON',
            'cb'        : 'done',
            'text'      : 'ВСЁ',
        }

        for f in fields: 
            field = None
            print("-- F TYPE IS ", f['type'].value)
            match f['type'].value:
                case FormType.REGULAR_TEXT:
                    field = RegularTextFormElem(f, self.regular_texts)
                case FormType.REGULAR_FIELD:
                    field = RegularFieldFormElem(f, self.regular_fields)
                case FormType.DYNAMIC_FIELD:
                    field = DynamicFieldFormElem(f, self.dynamic_fields)
                case FormType.BUTTON:
                    field = ButtonFormElem(f, self.buttons)
                case FormType.SINGLE_CHOICE:
                    field = SingleChoiceFormElem(f, self.single_choises)
                case FormType.MULTI_CHOICE:
                    field = MultiChoiceFormElem(f, self.multi_choises)
                case FormType.DOCUMENT:
                    field = DocumentFormElem(f, self.documents)
                case _:
                    print("NO MATCH!")
                    raise 'Cannot make form, unsupported type!'
            self.fields[f['id']] = field

    def IsCompleted(self) -> bool:
        for field in self.form:
            if not field.IsCompleted():
                return False
        return True

    def AcceptInput(self, input, storage) -> bool:
        field = self.fields[input['field_id']]
        field.AcceptInput(input, storage)

    def Reject(self, storage):
        for field in self.fields.values():
            field.Reject(storage)

    def ToDict(self) -> Dict:
        repr = list()
        for field in self.fields.values():
            repr.append( field.ToDict() )
        if self.can_go_prev:
            repr.append(self.prev_b_tpl)
        if self.can_go_next:
            repr.append(self.next_b_tpl)
        elif self.can_be_done:
            repr.append(self.done_b_tpl)
        return repr

    def ToJson(self) -> str:
        return json.dumps( self.ToDict() )


class FormPrototypeFactory():
    prototypes = dict()

    def INIT(states, fields):
        for state in states.values():
            print(" -- STATE FORMS IDS ARE ", state['forms_ids'])
            if state['forms_ids']:
                try:
                    FormPrototypeFactory.prototypes[state['id']] = Form(
                        state,
                        [ fields[f_id] for f_id in state['forms_ids'] ]
                    )
                except Exception as e:
                    print(e)
                except:
                    pass

    def MakeForm(id):
        from copy import deepcopy
        return deepcopy(FormPrototypeFactory.prototypes.get(id, None)) 


class State():
    def __init__(self, state, context):
        self.id     = state['id']
        self.state  = state
        self.form   = FormPrototypeFactory.MakeForm(state['id'])
        self.next_id= None
        self.context=context

        transitions = context.graph.transitions
        self.branches = [
            {'conds'         : transitions[tr_id]['form_elem_id'],
             'next_state_id' : transitions[tr_id]['target_id'] }
                for tr_id in state['transitions_ids']
        ]

        self.DetermineNextState()
        self.AdjustFormButtons() 

    def IsCompleted(self) -> bool:
        if self.state['force_completion']:
            return self.form.IsCompleted()
        return True

    def AcceptInput(self, input) -> bool:
        self.form.AcceptInput(input, self.context.storage)
        self.DetermineNextState()
        self.AdjustFormButtons()
        print( self.HasNext() )
        print( self.context.state_history.CanSwitchToNext() )

    def DetermineNextState(self):
        for branch in self.branches:
            if len(branch['conds']) == 0:
                self.next_id = branch['next_state_id']
                print(self.next_id)
                return self.next_id
            for cond in branch['conds']:
                print('Cond is', cond)
                if not self.context.storage.Contains(cond):
                    break
                self.next_id = branch['next_state_id']
                return self.next_id
        self.next_id = None
        return self.next_id

    def AdjustFormButtons(self):
        if self.context.state_history.CanSwitchToPrev():
            self.form.can_go_prev = True
        else:
            self.form.can_go_prev = False
        if self.HasNext() or self.context.state_history.CanSwitchToNext():
            self.form.can_go_next = True
        else:
            self.form.can_go_next = False
        if self.IsEnd():
            self.form.can_be_done = True
        else:
            self.form.can_be_done = False

    def GetForm(self):
        return self.form.ToJson()

    def TestGetForm(self):
        return self.form.ToDict()

    def GetNextId(self):
        return self.next_id

    def Reject(self):
        self.form.Reject(self.context.storage)

    def HasNext(self):
        return self.next_id is not None

    def IsEnd(self):
        return len(self.branches) == 0


class StateHistory():
    def __init__(self, context):
        self.history    = list()
        self.context    = context
        self.idx        = -1

    def GetCurrent(self):
        return self.history[self.idx]

    def CanSwitchToNext(self):
        return len(self.history)-1 > self.idx

    def CanSwitchToPrev(self):
        return self.idx > 0

    def SetNext(self, state_id):
        if self.CanSwitchToNext() and self.GetNextState().id == state_id:
            self.idx += 1
            return
        while len(self.history)-1 > self.idx:
            self.history.pop().Reject()

        self.idx += 1
        try:
            self.history.append( 
                State(self.context.graph.states[state_id], self.context))
        except:
            self.idx -= 1

    def SwitchToNext(self) -> State:
        if self.CanSwitchToNext():
            self.idx += 1
        else:
            raise "Cannot switch next -- no next!"

    def SwitchToPrev(self) -> State:
        if self.CanSwitchToPrev():
            self.idx -= 1
        else:
            raise "Cannot switch prev -- no prev!"

    def GetNextState(self):
        return self.history[self.idx+1]


class StateMachine():
    def __init__(self, context):
        self.context    = context

    def Go(self, input=None):
        self.DetermineNextState(input)
        return self.context.state_history.GetCurrent().GetForm()

    def TestGo(self, input=None):
        self.DetermineNextState(input)
        return self.context.state_history.GetCurrent().TestGetForm()

    def DetermineNextState(self, input):
        sh = self.context.state_history
        state = sh.GetCurrent()

        if input is None:
            pass
        elif input['field_id'] == 'next':
            if state.HasNext():
                next_id = state.GetNextId()
                sh.SetNext(next_id)
            else:
                sh.SwitchToNext()
        elif input['field_id'] == 'prev':
            sh.SwitchToPrev()
        elif input['field_id'] == 'done':
            print("WE ARE DONE!")
        else:
            state.AcceptInput(input)


class UserInputStorage():
    def __init__(self, fields):
        self.storage = dict()
        
        for field in fields.values():
            self.storage[field['id']] = None 

    def Write(self, key, value):
        self.storage[key] = value

    def Delete(self, key):
        self.storage[key] = None

    def Contains(self, key):
        return self.storage.get(key, None) is not None


class Context():
    def __init__(self, storage, graph):
        self.storage        = storage
        self.graph          = graph
        self.state_machine  = StateMachine(self)
        self.state_history  = StateHistory(self) 


        

from enum   import Enum, unique
@unique
class InputType(Enum):
    NEXT    = 'next',
    PREV    = 'prev',
    DONE    = 'done',
    FORM    = 'form',
    MENU    = 'menu',


from typing import TypedDict
class Input(TypedDict):
    type        : InputType
    session_id  : str
    field_id    : str
    cb          : str

