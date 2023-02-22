from ..keyboards    import TextMessage, InlineKeyboard, Form
class FormGroupFactory():
    @staticmethod
    def INIT():
        pass

    @staticmethod
    def Make(t, tg_user_id):
        if t == 'TEXT':
            return TextMessage(tg_user_id)
        return InlineKeyboard(tg_user_id)


class FormFactory():
    @staticmethod
    def INIT():
        pass

    @staticmethod
    def Make(form_description, tg_user_id):
        form        = Form(tg_user_id)
        prev_type   = None
        cur_group   = None 

        for elem in form_description:
            if elem['type'] != prev_type:
                form.AddGroup(cur_group)
                prev_type = elem['type']
                cur_group = FormGroupFactory.Make(prev_type, 
                                                  tg_user_id)
            cur_group.AddElem(elem)
        form.AddGroup(cur_group)

        return form

