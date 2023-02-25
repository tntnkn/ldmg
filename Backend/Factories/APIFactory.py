from ..APIs  import MonoAPI


class APIFactory():
    active_users  = None
    general_info  = None
    state_machine = None

    @staticmethod
    def INIT(active_users, general_info, state_machine):
        APIFactory.active_users  = active_users
        APIFactory.state_machine = state_machine
        APIFactory.general_info  = general_info

    @staticmethod
    def Make():
        return MonoAPI(APIFactory.active_users, 
                       APIFactory.general_info,
                       APIFactory.state_machine)

