from pyairtable  import Table
from typing      import Dict, Tuple
from .           import Config
from .State      import State, StateType
from .Transition import Transition, TransitionType, OperatorType, get_always_reachable_transition
from .Form       import Form, FormType
from .Types      import ID_TYPE
from .Graph      import Graph


class StateFieldsConsts():
    NAME                = 'Название'
    FORMS               = 'Форма'
    FORCE_COMPLETION    = 'Обязательно закончить'
    IS_START            = 'Начало'
    IS_END              = 'Конец'
    IS_ALWAYS_REACHABLE = 'Всегда доступно'
    PIN_WIDGET          = 'Закрепить виджет'
    BEFORE_ENTER        = 'Перед входом'
    BEFORE_LEAVE        = 'Перед уходом'


class TransitionFieldConsts():
    NAME                = 'Название'
    SOURCE              = 'Откуда'
    TARGET              = 'Куда'
    LEFT_COMP_OPER      = 'Эллемент формы'
    OPERATOR            = 'Оператор'
    RIGHT_COMP_OPER     = 'Значение'


class OperatorTypeFieldConst():
    NONE        = 'Отсутствует'
    EQUALS      = 'Равно'


class FormFieldConsts():
    NAME                = 'Название'
    TYPE                = 'Тип'
    VALUE               = 'Значение'


class Loader():
    def __init__(self):
        self.states_records         = list()
        self.transitions_records    = list()
        self.forms_records          = list()

        self.forms : Dict[ID_TYPE, Form] = dict()

        self.graph                  = Graph()

    def load_tables(self):
        config = Config.get()

        states_table        = Table(config.AIRTABLE_API_KEY, 
                                config.AIRTABLE_BASE_ID,
                                config.AIRTABLE_STATES_TABLE_ID)
        self.states_records = states_table.all() 
        if len(self.states_records) == 0:
            raise "States table is empty!"

        transitions_table   = Table(config.AIRTABLE_API_KEY, 
                                config.AIRTABLE_BASE_ID,
                                config.AIRTABLE_TRANSITIONS_TABLE_ID)
        self.transitions_records = transitions_table.all() 
        if len(self.transitions_records) == 0:
            raise "Transitions table is empty!"

        forms_table         = Table(config.AIRTABLE_API_KEY, 
                                config.AIRTABLE_BASE_ID,
                                config.AIRTABLE_FORMS_TABLE_ID)
        self.forms_records  = forms_table.all() 
        if len(self.forms_records) == 0:
            raise "Forms table is empty!"

    
    def load_graph(self):
        if len(self.states_records) == 0 or\
           len(self.transitions_records) == 0 or\
           len(self.forms_records) == 0:
               self.load_tables()

        self.process_states_records()
        self.process_transitions_records()
        self.process_forms_records()

        for state in self.graph.states.values():
            for reach_node_id in self.graph.always_reachable_nodes_ids:
                tr = get_always_reachable_transition(
                    state['id']+reach_node_id, 
                    state['id'],
                    reach_node_id)
                self.graph.AddTransition(tr)

    def process_states_records(self):
        for record in self.states_records:
            fields = record['fields']
            state : State = {
                'id' : record['id'],
                'name': fields.get(
                        StateFieldsConsts.NAME, 
                        'NO NAME PROVIDED!'),
                'type': StateType.UNKNOWN,
                'force_completion' : fields.get(
                        StateFieldsConsts.FORCE_COMPLETION, 
                        False),
                'forms_ids' : [
                    a_id for a_id in fields.get( 
                        StateFieldsConsts.FORMS, 
                        list() )],
                'is_start' : fields.get(
                        StateFieldsConsts.IS_START, 
                        False),
                'is_end' : fields.get(
                        StateFieldsConsts.IS_END, 
                        False),
                'is_always_reachable' : fields.get(
                        StateFieldsConsts.IS_ALWAYS_REACHABLE, 
                        False),
                'pin_widget' : fields.get(
                        StateFieldsConsts.PIN_WIDGET, 
                        False),
                'before_enter' : fields.get(
                        StateFieldsConsts.BEFORE_ENTER, 
                        False),
                'before_leave': fields.get(
                        StateFieldsConsts.BEFORE_LEAVE, 
                        False),
            }

            if   state['is_start']:
                state['type'] = StateType.START
            elif  state['is_end']:
                state['type'] = StateType.END
            elif state['is_always_reachable']:
                state['type'] = StateType.ALWAYS_REACHABLE
            else:
                state['type'] = StateType.REGULAR
            
            self.graph.AddState(state)
        return self.graph.transitions


    def process_transitions_records(self):
        transitions : Dict[ID_TYPE, Transition] = dict()
        for record in self.transitions_records:
            fields = record['fields']

            cond_operator =fields.get(TransitionFieldConsts.OPERATOR, '')
            match cond_operator:
                case OperatorTypeFieldConst.EQUALS:
                    cond_operator = OperatorType.EQUALS
                case _:
                    cond_operator = OperatorType.NONE

            transition : Transition = {
                    'id' : record['id'],
                    'name' : fields.get(
                        TransitionFieldConsts.NAME, None),
                    'type': TransitionType.UNKNOWN,
                    'source_id' : fields.get(
                        TransitionFieldConsts.SOURCE, None)[0],
                    'target_id' : fields.get(
                        TransitionFieldConsts.TARGET, None)[0],
                    'form_elem_id' : fields.get(
                        TransitionFieldConsts.LEFT_COMP_OPER, [None])[0],
                    'cond_operator' : cond_operator,
                    'cond_value' : fields.get(
                        TransitionFieldConsts.RIGHT_COMP_OPER, None),
            }
            if transition['form_elem_id']:
                transition['type'] = TransitionType.CONDITIONAL
            else:
                transition['type'] = TransitionType.UNCONDITIONAL

            self.graph.AddTransition(transition)
        return self.graph.transitions

    def process_forms_records(self):
        for record in self.forms_records:
            fields = record['fields']
            form : Form = {
                'id'    : record['id'],
                'name'  : fields.get(
                    FormFieldConsts.NAME, None),
                'type'  : FormType.UNKNOWN,
                'value' : fields.get(
                    FormFieldConsts.VALUE, None),
            }

            t = record['fields'].get(FormFieldConsts.TYPE, None)
            for ft in FormType:
                if ft.value == t:
                    form['type'] = ft
                    break
            if form['type'] == FormType.UNKNOWN:
                raise "Form type unknown!"

            self.forms[form['id']] = form



if __name__ == '__main__':
    from .State      import get_dummy_state
    from .Transition import get_dummy_transition
    from .Form       import get_dummy_form
    
    loader = Loader()
    loader.load_tables()
    print('\nSTATES RECORDS') 
    print(loader.states_records)
    print('\nTRANSACTIONS RECORDS') 
    print(loader.transitions_records)
    print('\FORMS RECORDS') 
    print(loader.forms_records)
    loader.process_states_records()
    loader.process_transitions_records()
    loader.process_forms_records()
    loader.load_graph()
    print('\n\n')
    print('STATES')
    for state in loader.graph.states.values():
        print(state,'\n')
    print('TRANSITIONS')
    for transition in loader.graph.transitions.values():
        print(transition, '\n')
    print('FORMS')
    for form in loader.forms.values():
        print(form, '\n')

