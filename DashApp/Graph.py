from typing         import Dict
from .Styling       import get_node_type_class, get_edge_type_class


class CytoGraph():
    def __init__(self, graph):
        self.start_node_id : Union[int, None] = None
        self.end_node_id   : Union[int, None] = None
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

        self.nodes : Dict[str, Dict] = dict()
        self.edges : Dict[str, Dict] = dict()

        for state in graph.states.values():
            self.AddNode(state)
        for transition in graph.transitions.values():
            self.AddEdge(transition)

    def AddNode(self, state) -> Dict:
        if state['id'] in self.nodes:
            return self.nodes['id'] 

        node = {
            'data': {
                'id'    : state['id'], 
                'label' : state['name']
            },
            'classes': get_node_type_class(state['type'].value),
        }

        self.nodes[node['data']['id']] = node        
        self.impl['elements']['nodes'].append(node)

        return node

    def AddEdge(self, transition) -> Dict:
        if transition['id'] in self.edges:
            return self.edges['id']

        edge = {
            'data': {
                'id'    : transition['id'],
                'label' : transition['name'],
                'source': transition['source_id'], 
                'target': transition['target_id'],
            },
            'classes'   : get_edge_type_class(transition['type'].value)
        }
       
        self.edges[edge['data']['id']] = edge
        self.impl['elements']['edges'].append(edge)

        return edge


if __name__ == '__main__':
    pass

