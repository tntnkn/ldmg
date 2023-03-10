from ..Form     import Form
from ..Storage  import Context, Models as M
from .          import FormElemFactory

from ..Types    import FormBehavior
from typing     import Dict

from copy       import deepcopy


class FormPrototypeFactory():
    prototypes: Dict[M.ID, Form] = dict()
    fields = None

    @staticmethod
    def INIT(states, fields):
        FormPrototypeFactory.fields = fields
        for state in states.values():
            #print(" -- STATE FORMS IDS ARE ", state['forms_ids'])
            #if state['forms_ids']:
            fields = \
                FormPrototypeFactory.__FieldsToFormElems(state['forms_ids'])
            FormPrototypeFactory.prototypes[state['id']] = \
                Form(state['id'], fields)

    @staticmethod
    def Make(form_id: M.ID) -> Form:
        from copy import deepcopy
        # THIS ONE IS NOW WORKING NOW
        # I know, I know, should've deleted it
        return deepcopy( FormPrototypeFactory.Get(form_id) )

    @staticmethod
    def Get(form_id: M.ID, context : Context) -> Form:
        form  = FormPrototypeFactory.prototypes[form_id]
        behav = context.forms_info.Read(form_id)['form_behavior']
        print("BEHAV", behav)
        if behav == FormBehavior.REGULAR:
            return form

        ids   = form.GetFieldsIds()
        inps  = context.user_input.ReadAll()
        ids.extend([
            k for k,v in inps.items() if isinstance(v, str)
        ])
        fields = FormPrototypeFactory.__FieldsToFormElems(ids)

        return Form(form.id, fields)

    @staticmethod
    def __FieldsToFormElems(fields_ids):
        pt      = None 
        fields  = list()
        for id in fields_ids:
            f, pt = FormElemFactory.Make(
                FormPrototypeFactory.fields[id],
                pt)
            fields.append(f)
        return fields

