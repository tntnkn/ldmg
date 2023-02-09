from typing      import Union, Dict
from .State      import State, StateType 
from .Transition import Transition
from .Form       import Form 
from .Exceptions import StartNodeAlreadyExists, EndNodeAlreadyExists, SourceNodeNotInGraph, TargetNodeNotInGraph
from .Types      import ID_TYPE


class Graph():
    def __init__(self):
        self.start_node_id : Union[ID_TYPE, None] = None
        self.end_node_id   : Union[ID_TYPE, None] = None
        self.always_open_ids : List[ID_TYPE]      = list()

        self.states      : Dict[ID_TYPE, State]      = dict()
        self.transitions : Dict[ID_TYPE, Transition] = dict()

    def AddState(self, state : State) -> State:
        if state['id'] in self.states:
            return state 

        if state['type'] == StateType.START and self.start_node_id:
            raise StartNodeAlreadyExists(state) 
        if state['type'] == StateType.END   and self.end_node_id:
            raise EndNodeAlreadyExists(state) 

        self.states[state['id']] = state

        if    state['type'] == StateType.START:
            self.start_node_id = state['id'] 
        elif  state['type'] == StateType.END:
            self.end_node_id   = state['id'] 
        elif  state['type'] == StateType.ALWAYS_OPEN:
            self.always_open_ids.append(state['id'])

        return state

    def AddTransition(self, 
                transition: Transition) -> Transition:
        if transition['id'] in self.transitions:
            return transition

        if not self.states.get(transition['source_id'], None):
            raise SourceNodeNotInGraph(transition['source_id'])
        if not self.states.get(transition['target_id'], None):
            raise TargetNodeNotInGraph(transition['target_id'])
        
        self.transitions[transition['id']] = transition

        return transition


if __name__ == '__main__':
    pass

