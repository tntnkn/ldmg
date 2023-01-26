import Graph
from Forms import FormPrototypeFactory, StateHistory

def main():
    print("Loading graph")
    graph = Graph.load_graph()
    forms = list()
    print("Building forms factory")
    
    form_factory = FormPrototypeFactory(
            graph.states.values(), 
            graph.transitions)

    print('\nForms are:')
    for form in form_factory.prototypes.values():
        print('- ', graph.states[form.id]['name'], form.fields, '\n')

    print('\nTesting prototype factory:')
    for form in form_factory.prototypes.values():
        copy = form_factory.MakeForm(form.id)
        print('- ', form.id, copy.id)
    for form in form_factory.prototypes.values():
        copy = form_factory.MakeForm(form.id)
        copy.id = 'LALALA'
        print('- ', form.id, copy.id)

    state_history = StateMachine(graph)
    currnet_state_id = graph.start_node_id
     
    while True:
        pass



if __name__ == '__main__':
    main()

