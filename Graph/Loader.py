from pyairtable  import Table
from typing      import Dict, Tuple
from .           import Config
from .State      import State, StateType
from .Transition import Transition, TransitionType 
from .Form       import Form, FormType
from .Types      import ID_TYPE
from .Graph      import Graph
from .Exceptions import UnknownFormType, TableIsEmpty
from .Models     import StateFieldsConsts, TransitionFieldConsts, FormFieldConsts


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
            raise TableIsEmpty('States')

        transitions_table   = Table(config.AIRTABLE_API_KEY, 
                                config.AIRTABLE_BASE_ID,
                                config.AIRTABLE_TRANSITIONS_TABLE_ID)
        self.transitions_records = transitions_table.all() 
        if len(self.transitions_records) == 0:
            raise TableIsEmpty('Transitions')

        forms_table         = Table(config.AIRTABLE_API_KEY, 
                                config.AIRTABLE_BASE_ID,
                                config.AIRTABLE_FORMS_TABLE_ID)
        self.forms_records  = forms_table.all() 
        if len(self.forms_records) == 0:
            raise TableIsEmpty('Forms')

    
    def load_graph(self):
        if len(self.states_records) == 0 or\
           len(self.transitions_records) == 0 or\
           len(self.forms_records) == 0:
               self.load_tables()

        self.process_states_records()
        self.process_transitions_records()
        self.process_forms_records()


    def process_states_records(self):
        for record in self.states_records:
            fields = record['fields']
            state : State = {
                'id'        : record['id'],
                'name'      : fields.get(
                        StateFieldsConsts.NAME, 'NO NAME'),
                'type'      : StateType.UNKNOWN,
                'is_start'  : False,
                'is_end'    : False,
                'forms_ids' : [
                    a_id for a_id in fields.get( 
                        StateFieldsConsts.FORMS, list() )],
                'in_transitions_ids' : [
                    a_id for a_id in fields.get( 
                        StateFieldsConsts.IN_TRANSITIONS, list() )],
                'out_transitions_ids' : [
                    a_id for a_id in fields.get( 
                        StateFieldsConsts.OUT_TRANSITIONS, list() )],
            }

            if   len(state['in_transitions_ids'])  == 0 and\
                 len(state['out_transitions_ids']) == 0:
                state['type'] = StateType.ALWAYS_OPEN
            elif len(state['in_transitions_ids'])  == 0:
                state['type'] = StateType.START
            elif len(state['out_transitions_ids']) == 0:
                state['type'] = StateType.END
            else:
                state['type'] = StateType.REGULAR
            
            self.graph.AddState(state)
        return self.graph.transitions


    def process_transitions_records(self):
        transitions : Dict[ID_TYPE, Transition] = dict()
        for record in self.transitions_records:
            fields = record['fields']

            transition : Transition = {
                    'id' : record['id'],
                    'name' : fields.get(
                        TransitionFieldConsts.NAME, 'NO NAME'),
                    'type': TransitionType.UNKNOWN,
                    'source_id' : fields.get(
                        TransitionFieldConsts.SOURCE, None)[0],
                    'target_id' : fields.get(
                        TransitionFieldConsts.TARGET, None)[0],
                    'form_elem_ids' : fields.get(
                        TransitionFieldConsts.FORM_CONDITIONS, list()),
            }
            if len(transition['form_elem_ids']) == 0:
                transition['type'] = TransitionType.UNCONDITIONAL
            else:
                transition['type'] = TransitionType.CONDITIONAL

            self.graph.AddTransition(transition)
        return self.graph.transitions


    def process_forms_records(self):
        for record in self.forms_records:
            fields = record['fields']
            form : Form = {
                'id'    : record['id'],
                'name'  : fields.get(
                    FormFieldConsts.NAME, 'NO NAME'),
                'type'  : FormType.UNKNOWN,
            }

            t = record['fields'].get(FormFieldConsts.TYPE, None)
            for ft in FormType:
                if ft.value == t:
                    form['type'] = ft
                    break
            if form['type'] == FormType.UNKNOWN:
                raise UnknownFormType(form['name'])

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

