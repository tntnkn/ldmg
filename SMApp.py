from Graph import Loader
from Forms import FormPrototypeFactory, Context, UserInputStorage, Input, State, StateFactory, UserDone

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


    StateFactory.INIT(State)

    print('\nCreating Context')
    storage = UserInputStorage(forms)
    context = Context(storage, graph)
    context.state_history.SetNext(graph.start_node_id)
    context.state_history.SwitchToNext()

    i = None
    try:
        while True:
            form = context.state_machine.TestGo(i)
            print('Form is', form)
            for f in form:
                print(f)
            mapping = print_form(form)
            i = get_input_to_return(mapping)
    except UserDone:
        for key, value in storage.storage.items():
            print(forms[key]['name'], ' - ', value)

def get_input_to_return(mapping) -> Input:
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

