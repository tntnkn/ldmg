from Graph              import Loader
from Backend.Factories  import Assembly


def main():

    print("Loading graph")
    loader = Loader()
    loader.load_graph()

    Assembly.Assemble(loader)
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
        elif reply['type'] == 'pos_end':
            for key, value in reply['contents']:
                print(loader.forms[key]['name'], ' - ', value)
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

