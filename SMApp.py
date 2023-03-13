from maxdmg_resource    import MaxDmgLoader 
from Backend            import Assembly

from dotenv             import load_dotenv
import os


class Config():
    def __init__(self):
        load_dotenv()

        self.AIRTABLE_API_KEY                       =\
            os.getenv('AIRTABLE_API_KEY')
        self.AIRTABLE_BASE_ID                       =\
            os.getenv('AIRTABLE_BASE_ID')
        self.AIRTABLE_STATES_TABLE_ID               =\
            os.getenv('AIRTABLE_STATES_TABLE_ID')
        self.AIRTABLE_STATES_TABLE_MAIN_VIEW_ID     =\
            os.getenv('AIRTABLE_STATES_TABLE_MAIN_VIEW_ID')
        self.AIRTABLE_TRANSITIONS_TABLE_ID          =\
            os.getenv('AIRTABLE_TRANSITIONS_TABLE_ID')
        self.AIRTABLE_TRANSITION_TABLE_MAIN_VIEW_ID =\
            os.getenv('AIRTABLE_TRANSITION_TABLE_MAIN_VIEW_ID')
        self.AIRTABLE_FORMS_TABLE_ID                =\
            os.getenv('AIRTABLE_FORMS_TABLE_ID')
        self.AIRTABLE_FORMS_TABLE_MAIN_VIEW_ID      =\
            os.getenv('AIRTABLE_FORMS_TABLE_MAIN_VIEW_ID')
        self.AIRTABLE_CONFIG_TABLE_ID               =\
            os.getenv('AIRTABLE_CONFIG_TABLE_ID')
        self.AIRTABLE_CONFIG_TABLE_MAIN_VIEW_ID     =\
            os.getenv('AIRTABLE_CONFIG_TABLE_MAIN_VIEW_ID')

config = Config()


def main():

    print("Loading graph")
    resp = MaxDmgLoader().LoadFromConfig(config)

    Assembly.Assemble(resp)
    back_api = Assembly.api 

    user_id = back_api.NewUser()
    message = {
        'user_id'   : user_id,
        'type'      : 'input',
        'contents'  : None,
    }

    while True:
        reply = back_api.AcceptInput(message)
        if   reply['type'] == 'form':
            form  = reply['contents']
            """
            print('Form is', form)
            for f in form:
                print(f)
            """
            mapping = print_form(form)
            message['contents'] = get_input_to_return(mapping)
        elif reply['type'] == 'doc_info':
            for key, value in reply['contents'].items():
                print(key, ' - ', value)
            print('WE ARE DONE!')
            break
        else:
            raise RuntimeError('UNKNOWN MESSAGE TYPE')


def get_input_to_return(mapping):
    i = input('Gimme input: ')

    if len(i) == 0:
        return None
    elif not i.isdigit():
        return None
    
    idx = int(i)
    if idx > len(mapping)-1:
        return None

    f = mapping[idx]
    ret =  {
            'field_type'    : f['type'],
            'field_id'      : f['id'],
            'cb'            : f['cb'],
    }

    if ret['field_type'] == 'FORM':
        ret['cb'] = input('Gimme smth to write to a form: ')
    elif ret['field_type'] == 'D_FORM' or\
         ret['field_type'] == 'D_FORM_CHIEF':
        ret['cb'] = input('Gimme smth to write to a form: ')
        ret['d_id'] = f['d_id']

    return ret


def print_form(form):
    print('\nFORM:')
    mapping = list()
    cnt = 0
    for field in form:
        print(cnt, field['completed'], field['text'], field['type'], field['cb'])
        mapping.append(field)
        cnt += 1
    return mapping
       


if __name__ == '__main__':
    main()

