from typing             import Dict
from Types              import FormType
import json


class FormElem():
    def __init__(self, field, group):
        self.id     = field['id']
        self.group  = group
        self.text   = field['name'] 
        self.desc   = ''
        self.cb     = field['id']
        self.completed  = False
        self.storage_id = field['id']

        self.group.append(self)

    def IsCompleted(self) -> bool:
        return self.completed

    def AcceptInput(self, input, context) -> bool:
        self.completed = True
        context.storage.Write(self.storage_id, input['cb'])
        return self.IsCompleted()

    def Reject(self, context):
        self.completed = False
        context.storage.Delete(self.storage_id)

    def ToDict(self) -> Dict:
        return {
            'id'    : self.id,
            'type'  : self.type,
            'cb'    : self.cb,
            'text'  : self.text,
            'completed' : self.completed,
        }
    def ToJson(self) -> str:
        return json.dumps( self.ToDict() )

    def AddRepr(self, where):
        where.append( self.ToDict() )


class RegularTextFormElem(FormElem):
    def __init__(self, field, group):
        super().__init__(field, group)
        self.completed  = True
        self.type       = 'TEXT'


class RegularFieldFormElem(FormElem):
    def __init__(self, field, group):
        super().__init__(field, group)
        self.type       = 'FORM'
        self.def_text   = self.text
        
    def AcceptInput(self, input, context) -> bool:
        if input['cb'] == '':
            self.Reject(context)
        else:
            super().AcceptInput(input, context)
            self.text = input['cb']

    def Reject(self, context):
        super().Reject(context)
        self.text = self.def_text


class DynamicFieldFormElem(FormElem):
    class D_RegularFieldFormElem(FormElem):
        def __init__(self, field, group):
            super().__init__(field, group)
            self.d_id   = field['d_id']
            self.type   = 'D_FORM'
        
        def AcceptInput(self, input, context) -> bool:
            if input['cb'] == '':
                self.Reject(context)
            else:
                self.text = input['cb']
                self.completed = True

        def Reject(self, storage):
            self.group.pop( self.group.index(self) )
            self.completed = False

        def ToDict(self) -> Dict:
            my_repr = super().ToDict()
            my_repr['d_id'] = self.d_id
            return my_repr

    def __init__(self, field, group):
        super().__init__(field, group)
        self.type       = 'D_FORM_CHIEF'
        self.d_fields   = list()
        self.d_id       = None
        self.last_d_id  = 0
        
    def AcceptInput(self, input, context):
        if input['d_id'] is not None:
            self.__InputToOldDField(input, context)
        else:
            self.__InputToNewDField(input)
        
        if len(self.d_fields) == 0:
            self.completed = False
        else:
            self.completed = True
            self.__StoreText(context)

    def ToDict(self) -> Dict:
        my_repr = super().ToDict()
        my_repr['d_id'] = self.d_id
        ret = list()
        ret.append(my_repr)
        for d_field in self.d_fields:
            ret.append( d_field.ToDict() )
        return ret

    def AddRepr(self, where):
        where.extend( self.ToDict() )

    def __InputToOldDField(self, input, context):
        for  d_field in self.d_fields:
            if d_field.d_id == input['d_id']:
                d_field.AcceptInput(input, context)
                ok = True
                return
        raise 'Dynamic field is not present!'

    def __InputToNewDField(self, input):
        if input['cb'] == '':
            return
        self.last_d_id += 1
        new_form_field = {
            'name'      : input['cb'],
            'desc'      : input['cb'],
            'id'        : self.id,
            'd_id'      : self.last_d_id,
        }
        DynamicFieldFormElem.D_RegularFieldFormElem(
                new_form_field, self.d_fields)

    def __StoreText(self, context):
        text = ''
        for d_field in self.d_fields:
            text += d_field.text + ', '
        text = text[:-2]
        context.storage.Write(self.storage_id, text)
         

class ButtonFormElem(FormElem):
    def __init__(self, field, group):
        super().__init__(field, group)
        self.type       = 'BUTTON'

    def AcceptInput(self, input, context) -> bool:
        super().AcceptInput(input, context)
        context.state_history.SetNext(
            context.branches.FieldIdToNextId(self.id) )
        context.state_history.SwitchToNext()


class SingleChoiceFormElem(FormElem):
    def __init__(self, field, group):
        super().__init__(field, group)
        self.type       = 'S_CHOICE'

    def AcceptInput(self, input, context) -> bool:
        if self.completed:
            self.Reject(context)
            return self.IsCompleted()
        for groupee in self.group:
            groupee.Reject(context)
        return super().AcceptInput(input, context)


class MultiChoiceFormElem(FormElem):
    def __init__(self, field, group):
        super().__init__(field, group)
        self.type       = 'M_CHOICE'

    def AcceptInput(self, input, context) -> bool:
        if self.completed:
            self.Reject(context)
            return self.IsCompleted()
        return super().AcceptInput(input, context)


class DocumentFormElem(FormElem):
    def __init__(self, field, group):
        super().__init__(field, group)
        self.type       = 'DOCUMENT'


from collections import OrderedDict
class Form():
    def __init__(self, state, fields):
        self.id             = state['id']
        self.fields         = OrderedDict()
        self.changed_fields = dict()

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

        regular_texts  = list()
        regular_fields = list()
        dynamic_fields = list()
        single_choises = list()
        multi_choises  = list()
        buttons        = list()
        documents      = list()

        for f in fields: 
            field = None
            print("-- F TYPE IS ", f['type'].value)
            match f['type'].value:
                case FormType.REGULAR_TEXT:
                    field = RegularTextFormElem(f, regular_texts)
                case FormType.REGULAR_FIELD:
                    field = RegularFieldFormElem(f,regular_fields)
                case FormType.DYNAMIC_FIELD:
                    field = DynamicFieldFormElem(f,dynamic_fields)
                case FormType.BUTTON:
                    field = ButtonFormElem(f, buttons)
                case FormType.SINGLE_CHOICE:
                    field = SingleChoiceFormElem(f,single_choises)
                case FormType.MULTI_CHOICE:
                    field = MultiChoiceFormElem(f,multi_choises)
                case FormType.DOCUMENT:
                    field = DocumentFormElem(f,documents)
                case _:
                    print("NO MATCH!")
                    raise 'Cannot make form, unsupported type!'
            self.fields[f['id']] = field

    def IsCompleted(self) -> bool:
        for field in self.form:
            if not field.IsCompleted():
                return False
        return True

    def IsFieldCompleted(self, field_id):
        return self.fields[field_id].IsCompleted()

    def AcceptInput(self, input, context) -> bool:
        field = self.fields[input['field_id']]
        field.AcceptInput(input, context)

    def Reject(self, context):
        for field in self.fields.values():
            field.Reject(context)

    def ToDict(self) -> Dict:
        import itertools 
        repr = list()
        for field in self.fields.values():
            field.AddRepr(repr)
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

    def Make(form_id):
        from copy import deepcopy
        return deepcopy(FormPrototypeFactory.prototypes.get(form_id, None))

class StateFactory():
    state_cls = None

    def INIT(state_cls):
        StateFactory.state_cls = state_cls

    def Make(state, context):
        return StateFactory.state_cls(state, context)


class Branch():
    def __init__(self, fields_ids, next_id):
        self.fields_ids    = fields_ids
        self.next_state_id = next_id

    def HasConditions(self):
        return len(self.fields_ids) != 0

    def HasCondition(self, field_id):
        return field_id in self.fields_ids

    def GetNextId(self):
        return self.next_state_id

    def GetConditions(self):
        return iter(self.fields_ids)


class StateBranches():
    def __init__(self, state, transitions):
        self.branches = [
            Branch(transitions[tr_id]['form_elem_id'],
                   transitions[tr_id]['target_id'])
                for tr_id in state['transitions_ids']
        ]
        self.form_id_cache = dict()

    def FieldIdToNextId(self, form_id):
        if form_id not in self.form_id_cache:
            self.form_id_cache[form_id] = self.__FindNextId(form_id)
        return self.form_id_cache[form_id]

    def __FindNextId(self, field_id):
        for branch in self.branches:
            if branch.HasCondition(field_id):
                return branch.GetNextId()
        raise f"No branch with field condition {form_id}"

    def __iter__(self):
        return iter(self.branches)

    def __len__(self):
        return len(self.branches)


class State():
    class ContextForForm():
        def __init__(self):
            self.state_history = None
            self.state_branches= None
            self.storage       = None

    def __init__(self, state, context):
        self.id       = state['id']
        self.state    = state
        self.branches = StateBranches(state, context.graph.transitions)
        self.next_id  = None
        self.context  = context
        self.form     = FormPrototypeFactory.Make(state['id'])

        self.form_context = self.__GetContextForForm(context)
        self.DetermineNextState()
        #print( self.HasNext() )
        #print( self.context.state_history.CanSwitchToNext() )

    def AcceptInput(self, input) -> bool:
        self.form.AcceptInput(input, self.form_context)
        self.DetermineNextState()
        #print( self.HasNext() )
        #print( self.context.state_history.CanSwitchToNext() )

    def Reject(self):
        self.form.Reject(self.form_context)

    def SetNext(self, next_id):
        self.next_id = next_id
        return self.next_id

    def GetNextId(self):
        return self.next_id

    def HasNext(self):
        return self.next_id is not None

    def GetForm(self):
        self.AdjustFormButtons()
        return self.form.ToJson()

    def TestGetForm(self):
        self.AdjustFormButtons()
        return self.form.ToDict()

    def IsEnd(self):
        return len(self.branches) == 0

    def DetermineNextState(self):
        for branch in self.branches:
            if not branch.HasConditions():
                return self.SetNext( branch.next_state_id )
            for cond in branch.GetConditions():
                print('Cond is', cond)
                if not self.form.IsFieldCompleted(cond):
                    break
                return self.SetNext( branch.next_state_id )
        return self.SetNext(None)

    def AdjustFormButtons(self):
        if self.context.state_history.CanSwitchToPrev():
            self.form.can_go_prev = True
        else:
            self.form.can_go_prev = False
        if self.HasNext():
            self.form.can_go_next = True
        else:
            self.form.can_go_next = False
        if self.IsEnd():
            self.form.can_be_done = True
        else:
            self.form.can_be_done = False

    def __GetContextForForm(self, context):
        form_context               = State.ContextForForm()
        form_context.state_history = context.state_history
        form_context.branches      = self.branches
        form_context.storage       = context.storage
        return form_context


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
            return state_id
        while len(self.history)-1 > self.idx:
            self.history.pop().Reject()
        self.history.append(StateFactory.Make(
            self.context.graph.states[state_id], self.context) )

    def SwitchToNext(self) -> State:
        if self.CanSwitchToNext():
            self.idx += 1
        else:
            raise "Cannot switch next -- no next!"

    def SwitchToPrev(self) -> State:
        self.__PrintHistory()
        if self.CanSwitchToPrev():
            self.idx -= 1
        else:
            raise "Cannot switch prev -- no prev!"

    def GetNextState(self):
        return self.history[self.idx+1]

    def __PrintHistory(self):
        print("History is: ")
        for state in self.history:
            print(state.id)


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
                sh.SetNext( state.GetNextId() )
            sh.SwitchToNext()
        elif input['field_id'] == 'prev':
            sh.SwitchToPrev()
        elif input['field_id'] == 'done':
            print("WE ARE DONE!")
            raise UserDone
        else:
            state.AcceptInput(input)

class UserDone(Exception):
    pass

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

