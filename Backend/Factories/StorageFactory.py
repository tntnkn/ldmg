from ..Storage  import Storage, Models
from typing     import Dict


class StorageFactory():
    graph = None
    forms: Dict
    docs : Dict

    @staticmethod
    def INIT(graph, forms, docs) -> None:
        StorageFactory.graph = graph
        StorageFactory.forms = forms
        StorageFactory.docs  = docs

    @staticmethod
    def Make() -> Storage:
        g = StorageFactory.graph

        user_input_model : Models.UserInput = dict()
        tags_by_field_id : Models.Tags      = dict()

        for field in StorageFactory.forms.values():
            if field['type'] == 'TEXT':
                continue
            user_input_model[field['id']] = None
            tags_by_field_id[field['id']] = field['tags']

        states_branches_storage : Models.StatesBranchesStorage = dict()
        possible_inp_ids : Models.PossibleInpIds = dict()
        states_names : Models.StatesNames = dict()

        for s_id, state in g.states.items():
            branches : Models.StateBranches = list()
            for tr_id in state['out_transitions_ids']:
                branch : Models.Branch = {
                    'type'               :
                        g.transitions[tr_id]['type'],
                    'req_user_input_ids' : 
                        g.transitions[tr_id]['form_elem_ids'],
                    'resulting_state_id' :
                        g.transitions[tr_id]['target_id'],
                }
                branches.append(branch)
            states_branches_storage[s_id] = branches
            possible_inp_ids[s_id] = state['forms_ids']
            states_names[s_id] = state['name']

        docs = [
            {'tag' : doc['tag'], 'doc_name' : doc['doc_name']} for\
                doc in StorageFactory.docs.values()
        ]
        
        general_info : Models.GeneralInfo = {
            # info for navigation 
            'start_id'          : g.start_node_id,
            'end_ids'           : g.end_node_ids,
            'always_open_ids'   : g.always_open_ids,
            # info for display (names, descriptions)
            'states_names'      : states_names,
            # info for branching
            'branches'          : states_branches_storage,
            'possible_inp_ids'  : possible_inp_ids, 
            # info for docgen
            'tags_by_field_id'  : tags_by_field_id,
            'documents'         : docs
        }
        return Storage(user_input_model, general_info)

