from ..Storage  import Storage, Models
from typing     import Dict


class StorageFactory():
    graph = None
    forms: Dict

    @staticmethod
    def INIT(graph, forms) -> None:
        StorageFactory.graph = graph
        StorageFactory.forms = forms

    @staticmethod
    def Make() -> Storage:
        g = StorageFactory.graph
        user_input_model : Models.UserInput = {
            field['id']: None for field in
                StorageFactory.forms.values() }
        states_branches_storage : Models.StatesBranchesStorage = dict()
        for s_id, state in g.states.items():
            branches : Models.StateBranches = list()
            for tr_id in state['transitions_ids']:
                branch : Models.Branch = {
                    'req_user_input_ids' : 
                        g.transitions[tr_id]['form_elem_id'],
                    'resulting_state_id' :
                        g.transitions[tr_id]['target_id'],
                }
                branches.append(branch)
            states_branches_storage[s_id] = branches
        general_info : Models.GeneralInfo = {
            'branches' : states_branches_storage,
            'start_id' : g.start_node_id,
        }
        return Storage(user_input_model, general_info)

