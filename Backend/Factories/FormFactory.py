from ..Form     import Form
from ..Storage  import Models as M
from typing     import Dict


class FormPrototypeFactory():
    prototypes: Dict[M.ID, Form] = dict()

    @staticmethod
    def INIT(states, fields):
        for state in states.values():
            #print(" -- STATE FORMS IDS ARE ", state['forms_ids'])
            if state['forms_ids']:
                FormPrototypeFactory.prototypes[state['id']]=Form(
                    state['id'],
                    [ fields[f_id] for f_id in state['forms_ids'] ]
                )

    @staticmethod
    def Make(form_id: M.ID) -> Form:
        from copy import deepcopy
        return deepcopy( FormPrototypeFactory.Get(form_id) )

    @staticmethod
    def Get(form_id: M.ID) -> Form:
        return FormPrototypeFactory.prototypes[form_id]

