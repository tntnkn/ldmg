from ..keyboards    import TextMessage, InlineKeyboard, Form
class FormGroupFactory():
    @staticmethod
    def INIT():
        pass

    @staticmethod
    def Make(t):
        if t == 'TEXT':
            return TextMessage()
        return InlineKeyboard()


class FormFactory():
    @staticmethod
    def INIT():
        pass

    @staticmethod
    def Make(form_description):
        form        = Form()
        prev_type   = None
        cur_group   = None 

        for elem in form_description:
            if elem['type'] != prev_type:
                form.AddGroup(cur_group)
                prev_type = elem['type']
                cur_group = FormGroupFactory.Make(prev_type)
            cur_group.AddElem(elem)
        form.AddGroup(cur_group)

        return form

