class StateHistory():
    def GetCurrent(context):
        idx = context.user_context.Read('current_state_idx')
        hst = context.user_context.Read('state_history')
        return hst[idx]

    def GetNext(context):
        idx = context.user_context.Read('current_state_idx') + 1
        hst = context.user_context.Read('state_history')
        return hst[idx]

    def SetNext(next_id, context):
        idx = context.user_context.Read('current_state_idx')
        hst = context.user_context.Read('state_history')
        print(idx)
        print(hst)
        if len(hst)-1 > idx and hst[idx+1]==next_id:
            return
        hst=hst[0:idx+1]
        print(hst)
        hst.append(next_id)
        print(hst)
        context.user_context.Write('state_history', hst)

    def DetermineNextState(context):
        cur_id   = StateHistory.GetCurrent(context)
        branches = context.general_info.Read('branches')[cur_id]
        u_input  = context.user_input

        for branch in branches:
            if len(branch['req_user_input_ids']) == 0:
                return branch['resulting_state_id']
            for inp in branch['req_user_input_ids']:
                print('Cond is', inp)
                if not u_input.Contains(inp):
                    break
                return branch['resulting_state_id']
        return None

    def AtEnd(context):
        cur_id   = StateHistory.GetCurrent(context)
        branches = context.general_info.Read('branches')[cur_id]
        return len(branches) == 0

    def CanSwitchToNext(context):
        idx = context.user_context.Read('current_state_idx')
        hst = context.user_context.Read('state_history')
        print(idx)
        print(len(hst))
        return len(hst)-1 > idx

    def CanSwitchToPrev(context):
        idx = context.user_context.Read('current_state_idx')
        return idx > 0

    def SwitchToNext(context):
        if StateHistory.CanSwitchToNext(context):
            idx = context.user_context.Read('current_state_idx')
            context.user_context.Write('current_state_idx', idx + 1)
        else:
            raise "Cannot switch next -- no next!"

    def SwitchToPrev(context):
        if StateHistory.CanSwitchToPrev(context):
            idx = context.user_context.Read('current_state_idx')
            context.user_context.Write('current_state_idx', idx - 1)
        else:
            raise "Cannot switch prev -- no prev!"

    def __PrintHistory(context):
        print("History is: ")
        pass

