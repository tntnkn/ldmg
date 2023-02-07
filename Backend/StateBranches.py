class Branch():
    def __init__(self, fields_ids, next_id):
        self.fields_ids    = fields_ids
        self.next_state_id = next_id

    def HasConditions(self):
        return len(self.fields_ids) != 0

    def HasCondition(self, field_id):
        return field_id in self.fields_ids

    def GetNextId(self):
        return self.next_state_id

    def GetConditions(self):
        return iter(self.fields_ids)


class StateBranches():
    def __init__(self, state, transitions):
        self.branches = [
            Branch(transitions[tr_id]['form_elem_id'],
                   transitions[tr_id]['target_id'])
                for tr_id in state['transitions_ids']
        ]
        self.form_id_cache = dict()

    def __DetermineNextState(self, context):
        branches = context.general_info.Read['branches']
        u_input  = context.user_input

        for branch in self.branches:
            if len(branch['req_user_input_ids']) == 0:
                return state_history.SetNext(branch['resulting_state_id'])
            for inp in branch['req_user_input_ids']:
                print('Cond is', inp)
                if not u_input.Contains[inp]:
                    break
                return state_history.SetNext(branch['resulting_state_id'])
        return state_history.SetNext(None)

    def FieldIdToNextId(self, form_id):
        if form_id not in self.form_id_cache:
            self.form_id_cache[form_id] = self.__FindNextId(form_id)
        return self.form_id_cache[form_id]

    def __FindNextId(self, field_id):
        for branch in self.branches:
            if branch.HasCondition(field_id):
                return branch.GetNextId()
        raise f"No branch with field condition {form_id}"

    def __iter__(self):
        return iter(self.branches)

    def __len__(self):
        return len(self.branches)

