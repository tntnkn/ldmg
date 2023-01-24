from typing      import TypedDict, List, Union, Dict
from .State      import State, get_dummy_state
from .Transition import Transition, get_always_reachable_transition, get_dummy_transition
from .Exceptions import NodeAlreadyInGraph, StartNodeAlreadyExists
from .Styling    import get_node_type_class, get_edge_type_class


class Graph():
    def __init__(self,
                 states:Dict[int,State],
                 transitions:Dict[int,Transition]):
        self.start_node_id : Union[int, None] = None
        self.always_reachable_nodes_ids : List[int] = list()

        self.impl = {
            'data'      : list(),
            'directed'  : True,
            'multigraph': False,
            'elements'  : {
                'nodes':  list(),
                'edges':  list(),
            },
        }

        self.states : Dict[int, Dict] = dict()
        self.transitions : Dict[int, Dict] = dict()

        for key, state in states.items():
            node = self.AddNode(state) 
            for transition_id in state['actions_ids']:
                transition = transitions[transition_id]
                if transition['next_state_id']:
                    next_node = self.AddNode(
                            states[transition['next_state_id']])
                    edge = self.AddEdge(node, next_node, transition)
        for node in self.impl['elements']['nodes']:
            for reach_node_id in self.always_reachable_nodes_ids:
                tr = get_always_reachable_transition(
                    node['data']['id']+reach_node_id, reach_node_id)
                self.AddEdge(node, 
                             self.AddNode(states[reach_node_id]),
                             tr)


    def MakeGraph(self,
                  states:Dict[int,State],
                  transitions:Dict[int,Transition]):
        pass


    def AddNode(self, state : State) -> Dict:
        if state['id'] in self.states:
            return state['graph_elem'] 

        if state['is_start'] and self.start_node_id:
            raise StartNodeAlreadyExists(state) 

        node = {
            'data': {
                'id'    : state['id'], 
                'label' : state['name']
            },
            'classes': get_node_type_class(state),
        }

        state['graph_elem'] = node
        self.states[state['id']] = state        
        self.impl['elements']['nodes'].append(node)

        if  state['is_start'] and not self.start_node_id:
            self.start_node_id = state['id'] 
            self.always_reachable_nodes_ids.append(state['id'])
        elif state['is_always_reachable']:
            self.always_reachable_nodes_ids.append(state['id'])

        return node

    def AddEdge(self, 
                source: Dict, 
                target: Dict, 
                transition: Transition) -> Dict:
        if transition['id'] in self.transitions:
            return transition['graph_elem']

        edge = {
            'data': {
                'id'    : transition['id'],
                'label' : transition['name'],
                'source': source['data']['id'], 
                'target': target['data']['id'],
            },
            'classes'   : get_edge_type_class(transition)
        }
       
        transition['graph_elem'] = edge
        self.transitions[transition['id']] = transition
        self.impl['elements']['edges'].append(edge)

        return edge


if __name__ == '__main__':
    states = { 0: get_dummy_state() }
    transactions = { 0: get_dummy_transition() }
    graph = Graph(states,transactions)
    print(graph)
    print(type(graph.impl['elements']['nodes'])) 
    print(graph.impl['elements']['nodes'][0])
    for node in graph.impl['elements']['nodes']:
        print(node)

