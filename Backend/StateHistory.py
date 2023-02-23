from .Exceptions    import CantSwitch
from .Storage       import Models as M
from .Storage       import Context 
from typing         import Union


class StateHistory():
    @staticmethod
    def GetCurrent(context: Context) -> M.ID:
        idx = context.user_context.Read('current_state_idx')
        hst = context.user_context.Read('state_history')
        return hst[idx]

    @staticmethod
    def GetNext(context: Context) -> M.ID:
        idx = context.user_context.Read('current_state_idx') + 1
        hst = context.user_context.Read('state_history')
        return hst[idx]

    @staticmethod
    def SetNext(next_id, context: Context) -> None:
        idx = context.user_context.Read('current_state_idx')
        hst = context.user_context.Read('state_history')
        if len(hst)-1 > idx and hst[idx+1]==next_id:
            return
        hst=hst[0:idx+1]
        if next_id:
            hst.append(next_id)
        context.user_context.Write('state_history', hst)
        return 
    """
    @staticmethod
    def DetermineNextState(context: Context) -> Union[M.ID, None]:
        cur_id   = StateHistory.GetCurrent(context)
        branches = context.general_info.Read('branches')[cur_id]
        u_input  = context.user_input
        all_inps = context.general_info.Read(
                'possible_inp_ids')[cur_id]

        for branch in branches:
            print(branch['type'].value)
            match branch['type'].value:
                case BranchTypes.CONDITIONAL:
                    for inp in branch['req_user_input_ids']:
                        if not u_input.Contains(inp):
                            break
                    else:
                        return branch['resulting_state_id']
                case BranchTypes.UNCONDITIONAL:
                    return branch['resulting_state_id']
                case BranchTypes.STRICT:
                    print('IN STRICT!')
                    for inp in all_inps:
                        print(inp)
                        if not u_input.Contains(inp):
                            break
                        print(inp, 'is OK!')
                    else:
                        return branch['resulting_state_id']

            if len(branch['req_user_input_ids']) == 0:
                return branch['resulting_state_id']
            for inp in branch['req_user_input_ids']:
                if not u_input.Contains(inp):
                    break
                return branch['resulting_state_id']
        return None
    """
    @staticmethod
    def AtEnd(context: Context) -> bool:
        cur_id   = StateHistory.GetCurrent(context)
        end_ids  = context.general_info.Read('end_ids')
        return cur_id in end_ids
        #branches = context.general_info.Read('branches')[cur_id]
        #return len(branches) == 0

    @staticmethod
    def CanSwitchToNext(context: Context) -> bool:
        idx = context.user_context.Read('current_state_idx')
        hst = context.user_context.Read('state_history')
        return len(hst)-1 > idx

    @staticmethod
    def CanSwitchToPrev(context: Context) -> bool:
        idx = context.user_context.Read('current_state_idx')
        return idx > 0

    @staticmethod
    def SwitchToNext(context: Context) -> None:
        if StateHistory.CanSwitchToNext(context):
            idx = context.user_context.Read('current_state_idx')
            context.user_context.Write('current_state_idx', idx + 1)
        else:
            raise CantSwitch("No next!")

    @staticmethod
    def SwitchToPrev(context: Context) -> None:
        if StateHistory.CanSwitchToPrev(context):
            idx = context.user_context.Read('current_state_idx')
            context.user_context.Write('current_state_idx', idx - 1)
        else:
            raise CantSwitch("No prev!")

