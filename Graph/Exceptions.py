class NodeAlreadyInGraph(Exception):
    def __init__(self, node):
        self.message    = 'Node is already added into graph!'
        self.node       = node

        super(NodeAlreadyInGraph, self).__init__( (self.message, node) )

    def __reduce__(self):
        return (NodeAlreadyInGraph, (self.message, self.node))


class StartNodeAlreadyExists(Exception):
    def __init__(self, node):
        self.message    = 'Start node is already added into graph!'
        self.node       = node

        super(StartNodeAlreadyExists, self).__init__( (self.message, node) )

    def __reduce__(self):
        return (StartNodeAlreadyExists, (self.message, self.node))


class EndNodeAlreadyExists(Exception):
    def __init__(self, node):
        self.message    = 'End node is already added into graph!'
        self.node       = node

        super(EndNodeAlreadyExists, self).__init__( (self.message, node) )

    def __reduce__(self):
        return (EndNodeAlreadyExists, (self.message, self.node))
