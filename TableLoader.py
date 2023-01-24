from pyairtable import Table
import Config
from typing     import Dict, Tuple
from State      import State, StateType
from Transition import Transition, TransitionType


class StateFieldsConsts():
    NAME                = 'Название'
    DEFAULT_NEXT_STATE  = 'Следующее по умолчанию'
    FORCE_COMPLETION    = 'Обязательно закончить'
    ACTIONS             = 'Действия'
    IS_START            = 'Начало'
    IS_ALWAYS_REACHABLE = 'Всегда доступно'
    DELETES_W_HISTORY_F = 'Удалить историю состояний при входе'
    DELETES_W_BEFORE_SW = 'Удалить виджет перед переключением'
    DELETES_W_UPON_END  = 'Удалить виджет в конце сессии'


class TransitionFieldConsts():
    NAME                = 'Название'
    TYPE                = 'Тип'
    PROPERTY_NAME       = 'Свойство'
    VALUE_NAME          = 'Значение'
    NEXT_STATE          = 'Следующее состояние'


def load_tables():
    config = Config.get()

    states_table    = Table(config.AIRTABLE_API_KEY, 
                            config.AIRTABLE_BASE_ID,
                            config.AIRTABLE_STATES_TABLE_ID)
    states_records  = states_table.all() 
    if len(states_records) == 0:
        raise "States table is empty!"

    transitions_table   = Table(config.AIRTABLE_API_KEY, 
                            config.AIRTABLE_BASE_ID,
                            config.AIRTABLE_TRANSITIONS_TABLE_ID)
    transitions_records = transitions_table.all() 
    if len(transitions_records) == 0:
        raise "Transitions table is empty!"

    return states_records, transitions_records


def process_states_records(states_records) -> Dict[int,State]:
    states : Dict[int,State] = dict()
    for record in states_records:
        fields = record['fields']
        state : State = {
            'id' : record['id'],
            'name': fields.get(
                    StateFieldsConsts.NAME, 'NO NAME PROVIDED!'),
            'graph_elem' : None,
            'type': StateType.UNKNOWN,
            'force_completion' : fields.get(
                    StateFieldsConsts.FORCE_COMPLETION, False),
            'actions_ids' : [a_id for 
                    a_id in fields.get( StateFieldsConsts.ACTIONS, list() )],
            'is_start' : fields.get(
                    StateFieldsConsts.IS_START, False),
            'is_always_reachable' : fields.get(
                    StateFieldsConsts.IS_ALWAYS_REACHABLE, False),
            'deletes_widget_history_force' : fields.get(
                    StateFieldsConsts.DELETES_W_HISTORY_F, False),
            'deletes_widget_before_switch' : fields.get(
                    StateFieldsConsts.DELETES_W_BEFORE_SW, False),
            'deletes_widget_upon_session_end': fields.get(
                    StateFieldsConsts.DELETES_W_UPON_END, False),
        }

        if   state['is_start']:
            state['type'] = StateType.START
        elif state['is_always_reachable']:
            state['type'] = StateType.ALWAYS_REACHABLE
        else:
            state['type'] = StateType.REGULAR

        states[state['id']] = state
    return states


def process_transitions_records(transitions_records) -> Dict[int,Transition]:
    transitions : Dict[int,Transition] = dict()
    for record in transitions_records:
        fields = record['fields']
        transition : Transition = {
                'id' : record['id'],
                'name' : fields.get(
                    TransitionFieldConsts.NAME, None),
                'graph_elem' : None,
                'type':TransitionType.UNKNOWN,
                'property_name' : fields.get(
                    TransitionFieldConsts.PROPERTY_NAME, None),
                'value' : fields.get(
                    TransitionFieldConsts.VALUE_NAME, None),
                'next_state_id' : None,
        }
        list_ids = fields.get(TransitionFieldConsts.NEXT_STATE, None) 
        if(list_ids):
            transition['next_state_id'] = list_ids[0]

        t = record['fields'].get(TransitionFieldConsts.TYPE, None)
        for at in TransitionType:
            if at.value == t:
                transition['type'] = at
                break
        if transition['type'] == TransitionType.UNKNOWN:
            raise "Transition type unknown!"
        transitions[transition['id']] = transition
    return transitions        

def process_records(states_records, transitions_records) ->\
        Tuple[ Dict[int, State], Dict[int, Transition] ]:
            pass

if __name__ == '__main__':
    from State      import get_dummy_state
    from Transition import get_dummy_transition

    s_r, t_r = load_tables()
    print('\nSTATES RECORDS') 
    print(s_r)
    print('\nTRANSACTIONS RECORDS') 
    print(t_r)
    states : Dict[int,State] = process_states_records(s_r)
    transitions : Dict[int,Transition] = process_transitions_records(t_r)
    print('\n\n')
    print('STATES')
    for state in states.values():
        print(state,'\n')
    print('TRANSITIONS')
    for transition in transitions.values():
        print(transition, '\n')

