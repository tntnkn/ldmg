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
            print_form( context.state_machine.TestGo(i) ) 
            i = get_input()
    except UserDone:
        print(storage.storage)


def get_input() -> Input:
    i = input('Gimme input: ')
    if len(i) == 0:
        i = None
    return {
        'type'          : 'dunno',
        'session_id'    : None,
        'field_id'      : i,
        'cb'            : i,
    }

def print_form(form):
    print('\nFORM:')
    for field in form:
        print(field['text'], field['type'], field['cb'])
        

if __name__ == '__main__':
    main()

