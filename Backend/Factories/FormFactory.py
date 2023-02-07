from ..Form    import Form


class FormPrototypeFactory():
    prototypes = dict()

    def INIT(states, fields):
        for state in states.values():
            print(" -- STATE FORMS IDS ARE ", state['forms_ids'])
            if state['forms_ids']:
                FormPrototypeFactory.prototypes[state['id']]=Form(
                    state['id'],
                    [ fields[f_id] for f_id in state['forms_ids'] ]
                )

    def Make(form_id):
        from copy import deepcopy
        return deepcopy( FormPrototypeFactory.Get(form_id) )

    def Get(form_id):
        return FormPrototypeFactory.prototypes[form_id]

