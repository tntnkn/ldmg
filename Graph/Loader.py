from pyairtable  import Table
from typing      import Dict, Tuple
from .           import Config
from .State      import State, StateType
from .Transition import Transition, TransitionType 
from .Form       import Form, FormType
from .Types      import ID_TYPE
from .Graph      import Graph
from .Exceptions import UnknownFormType, TableIsEmpty
from .Models     import StateFieldsConsts, TransitionFieldConsts, TransitionTypesConsts, FormFieldConsts


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
                                config.AIRTABLE_FORMS_TABLE_ID,
                                )
        self.forms_records  = forms_table.all(
            view=config.AIRTABLE_FORMS_TABLE_MAIN_VIEW_ID)
        if len(self.forms_records) == 0:
            raise TableIsEmpty('Forms')

    
    def load_graph(self):
        if len(self.states_records) == 0 or\
           len(self.transitions_records) == 0 or\
           len(self.forms_records) == 0:
               self.load_tables()

        s = self.process_states_records()
        t = self.process_transitions_records()
        f = self.process_forms_records()

        self.connect_states_with_forms(s, f)


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
                'forms_ids' : list(), 
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
        return self.graph.states


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

            cond = fields.get(
                TransitionFieldConsts.TRANSITION_CONDITION)
            match cond:
                case TransitionTypesConsts.CONDITIONAL:
                    transition['type']=TransitionType.CONDITIONAL
                case TransitionTypesConsts.UNCONDITIONAL:
                    transition['type']=TransitionType.UNCONDITIONAL
                case TransitionTypesConsts.STRICT:
                    transition['type']=TransitionType.STRICT
                case _:
                    raise RuntimeError(
                      'Transitions does not have a condition set')

            self.graph.AddTransition(transition)
        return self.graph.transitions


    def process_forms_records(self):
        for record in self.forms_records:
            fields = record['fields']
            form : Form = {
                'id'        : record['id'],
                'name'      : fields.get(
                    FormFieldConsts.NAME, 'NO NAME'),
                'type'      : FormType.UNKNOWN,
                'state_id'  : fields.get(
                    FormFieldConsts.STATE_ID, None),
                'tags'      : fields.get(
                    FormFieldConsts.TAGS, None),
            }

            t = record['fields'].get(FormFieldConsts.TYPE, None)
            for ft in FormType:
                if ft.value == t:
                    form['type'] = ft
                    break
            if form['type'] == FormType.UNKNOWN:
                raise UnknownFormType(form['name'])

            if form['state_id']:
                form['state_id'] = form['state_id'][0]

            self.forms[form['id']] = form
        return self.forms


    def connect_states_with_forms(self, states: Dict, forms: Dict):
        for form in forms.values():
            state = states.get(form['state_id'], None)
            if state:
                state['forms_ids'].append(form['id'])


def load_forms():
    l = Loader()
    l.load_tables()
    forms = l.process_forms_records()
    for form in forms.values():
        print(form['name'], form['type'])


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

