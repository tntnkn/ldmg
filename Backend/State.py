from .Factories     import FormPrototypeFactory
from .Interface     import FormContext
from .StateBraches  import StateBranches


class State():

    def __init__(self, state, context):
        self.id       = state['id']
        self.state    = state
        self.branches = StateBranches(state, context.graph.transitions)
        self.next_id  = None
        self.context  = context
        self.form     = FormPrototypeFactory.Make(state['id'])

        self.form_context = FormContext(context, self.branches)
        self.__DetermineNextState()

        #print( self.HasNext() )
        #print( self.context.state_history.CanSwitchToNext() )

    def AcceptInput(self, input) -> bool:
        self.form.AcceptInput(input, self.form_context)
        self.__DetermineNextState()
        #print( self.HasNext() )
        #print( self.context.state_history.CanSwitchToNext() )

    def Reject(self):
        self.form.Reject(self.form_context)

    def SetNext(self, next_id):
        self.next_id = next_id
        return self.next_id

    def GetNextId(self):
        return self.next_id

    def HasNext(self):
        return self.next_id is not None

    def HasPrev(self):
        return self.state['is_start'] is False

    def IsEnd(self):
        return len(self.branches) == 0

    def GetForm(self):
        self.__AdjustFormButtons()
        return self.form.ToJson()

    def TestGetForm(self):
        self.AdjustFormButtons()
        return self.form.ToDict()

    def __DetermineNextState(self):
        for branch in self.branches:
            if not branch.HasConditions():
                return self.SetNext( branch.next_state_id )
            for cond in branch.GetConditions():
                print('Cond is', cond)
                if not self.form.IsFieldCompleted(cond):
                    break
                return self.SetNext( branch.next_state_id )
        return self.SetNext(None)

    def __AdjustFormButtons(self):
        if self.HasPrev():
            self.form.can_go_prev = True
        else:
            self.form.can_go_prev = False
        if self.HasNext():
            self.form.can_go_next = True
        else:
            self.form.can_go_next = False
        if self.IsEnd():
            self.form.can_be_done = True
        else:
            self.form.can_be_done = False

