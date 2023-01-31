from typing      import TypedDict, List, Union, Dict
from .State      import State, get_dummy_state
from .Transition import Transition, get_always_reachable_transition, get_dummy_transition
from .Form       import Form, get_dummy_form
from .Exceptions import NodeAlreadyInGraph, StartNodeAlreadyExists, EndNodeAlreadyExists
from .Types      import ID_TYPE


class Graph():
    def __init__(self):
        self.start_node_id : Union[ID_TYPE, None] = None
        self.end_node_id   : Union[ID_TYPE, None] = None
        self.always_reachable_nodes_ids : List[ID_TYPE] = list()

        self.states : Dict[ID_TYPE, State] = dict()
        self.transitions : Dict[ID_TYPE, Transition] = dict()


    def AddState(self, state : State) -> State:
        if state['id'] in self.states:
            return state 

        if state['is_start'] and self.start_node_id:
            raise StartNodeAlreadyExists(state) 
        if state['is_end'] and self.end_node_id:
            raise EndNodeAlreadyExists(state) 

        self.states[state['id']] = state

        if  state['is_start'] and not self.start_node_id:
            self.start_node_id = state['id'] 
            self.always_reachable_nodes_ids.append(state['id'])
        elif  state['is_end'] and not self.end_node_id:
            self.end_node_id = state['id'] 
        elif state['is_always_reachable']:
            self.always_reachable_nodes_ids.append(state['id'])

        return state

    def AddTransition(self, 
                transition: Transition) -> Transition:
        if transition['id'] in self.transitions:
            return transition

        if not self.states.get(transition['source_id'], None):
            raise 'Source node not in graph!'
        if not self.states.get(transition['target_id'], None):
            raise 'Target node not in graph!'
        
        self.transitions[transition['id']] = transition
        self.states[transition['source_id']]['transitions_ids'].append(
                transition['id'])

        return transition


if __name__ == '__main__':
    pass

