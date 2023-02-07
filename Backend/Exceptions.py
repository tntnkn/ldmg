class FormElemSwitchedHistory(Exception):
    def __init__(self, form_elem_name):
        self.message = 'Form Element switched history to next state!'
        self.name    = form_elem_name

        super(FormElemSwitchedHistory, self).__init__( 
            (self.message, self.name) )

    def __reduce__(self):
        return (FormElemSwitchedHistory, (self.message, self.name))

