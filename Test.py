class Graph():
    def __init__(self):
        self.impl = {
            'data'      : list(),
            'directed'  : False,
            'multigraph': False,
            'elements'  : {
                'nodes':  list(),
                'edges':  list(),
            },
        }

        for node in self.impl['elements']['nodes']:
            print(node)


graph = Graph()
