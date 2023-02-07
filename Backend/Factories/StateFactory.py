from ..State    import State

class StateFactory():
    state_cls = None

    def INIT(state_cls):
        #temporarily deprecated
        StateFactory.state_cls = state_cls

    def Make(state, context):
        return State(state, context)

