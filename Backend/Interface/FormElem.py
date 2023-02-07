from ..StateHistory     import StateHistory


class FormElem():
    def __init__(self, field, group):
        self.id     = field['id']
        self.group  = group
        self.text   = field['name'] 
        self.desc   = ''
        self.cb     = field['id']
        self.storage_id = field['id']

        self.group.append(self)

    def AcceptInput(self, input, context):
        context.user_input.Write(self.storage_id, input['cb'])

    def Reject(self, context):
        context.user_input.Delete(self.storage_id)

    def IsCompleted(self, context):
        return True if context.user_input.Contains(self.storage_id) else False

    def ToDict(self, context):
        return {
            'id'        : self.id,
            'type'      : self.type,
            'cb'        : self.cb,
            'text'      : self.text,
            'completed' : self.IsCompleted(context),

        }
    def ToJson(self, context):
        return json.dumps( self.ToDict(context) )

    def AddRepr(self, where, context):
        where.append( self.ToDict(context) )

    def FormElemToNext(self, context):
        cur_id = StateHistory.GetCurrent(context)
        branches = context.general_info.Read('branches')[cur_id]
        for branch in branches:
            print(branch)
            for user_input_id in branch['req_user_input_ids']:
                if user_input_id == self.storage_id:
                    return branch['resulting_state_id']
        raise f"No branch with field condition {form_elem_id}"

