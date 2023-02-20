from ..APIs  import MonoAPI


class APIFactory():
    active_users  = None
    state_machine = None

    @staticmethod
    def INIT(active_users, state_machine):
        APIFactory.active_users  = active_users
        APIFactory.state_machine = state_machine

    @staticmethod
    def Make():
        return MonoAPI(APIFactory.active_users, 
                       APIFactory.state_machine)

