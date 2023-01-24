class NodeAlreadyInGraph(Exception):
    def __init__(self, node):
        self.message    = 'Node is already added into graph!'
        self.node       = node

        super(NodeAlreadyInGraph, self).__init__( (self.message, node) )

    def __reduce__(self):
        return (MyException, (self.message, self.node))


class StartNodeAlreadyExists(Exception):
    def __init__(self, node):
        self.message    = 'Start node is already added into graph!'
        self.node       = node

        super(StartNodeAlreadyExists, self).__init__( (self.message, node) )

    def __reduce__(self):
        return (MyException, (self.message, self.node))

