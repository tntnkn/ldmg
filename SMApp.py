from Graph              import Loader
from Backend.Factories  import FormPrototypeFactory, StorageFactory, ActiveUsersFactory
from Backend.StateMachine import StateMachine, UserDone


def main():
    print("Loading graph")
    loader = Loader()
    loader.load_graph()
    graph = loader.graph
    forms = loader.forms
    print("Building forms factory")
    
    FormPrototypeFactory.INIT(graph.states, forms)

    print('\nForms are:')
    for form in FormPrototypeFactory.prototypes.values():
        print('- ', graph.states[form.id]['name'], form.fields, '\n')

    print('\nTesting prototype factory:')
    for form in FormPrototypeFactory.prototypes.values():
        copy = FormPrototypeFactory.Make(form.id)
        print('- ', form.id, copy.id)
    for form in FormPrototypeFactory.prototypes.values():
        copy = FormPrototypeFactory.Make(form.id)
        copy.id = 'LALALA'
        print('- ', form.id, copy.id)

    StorageFactory.INIT(graph, forms)
    storage = StorageFactory.Make()
    ActiveUsersFactory.INIT(storage)
    active_users = ActiveUsersFactory.Make()

    user_id = 0
    active_users.AddUser(user_id)
    context = active_users.GetUserContext(user_id)

    SM = StateMachine()    
    i = None
    try:
        while True:
            form = SM.Go(context, i)
            print('Form is', form)
            for f in form:
                print(f)
            mapping = print_form(form)
            i = get_input_to_return(mapping)
    except UserDone:
        for key, value in context.user_input.storage.items():
            print(forms[key]['name'], ' - ', value)

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
            'type'          : f['type'],
            'session_id'    : None,
            'field_id'      : f['id'],
            'cb'            : f['cb'],
    }

    if ret['type'] == 'FORM':
        ret['cb'] = input('Gimme smth to write to a form: ')
    elif ret['type'] == 'D_FORM' or ret['type'] == 'D_FORM_CHIEF':
        ret['cb'] = input('Gimme smth to write to a form: ')
        ret['d_id'] = f['d_id']

    return ret


def print_form(form):
    print('\nFORM:')
    mapping = list()
    cnt = 0
    for field in form:
        print(cnt, field['text'], field['type'], field['cb'])
        mapping.append(field)
        cnt += 1
    return mapping
       


if __name__ == '__main__':
    main()

