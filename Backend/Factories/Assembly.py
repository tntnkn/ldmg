from Backend.Factories  import FormPrototypeFactory, StorageFactory, ActiveUsersFactory, APIFactory
from Backend.StateMachine import StateMachine 


class Assembly():
    storage         = None
    active_users    = None
    api             = None

    graph           = None
    forms           = None

    @staticmethod
    def Assemble(loader):
        graph = loader.graph
        forms = loader.forms
        Assembly.graph = graph
        Assembly.forms = forms

        print("Building forms factory")
        FormPrototypeFactory.INIT(graph.states, forms)
        Assembly.__PrintFormPrototypes()

        StorageFactory.INIT(graph, forms)
        Assembly.storage = StorageFactory.Make()
        ActiveUsersFactory.INIT(Assembly.storage)
        Assembly.active_users = ActiveUsersFactory.Make()
        
        APIFactory.INIT(Assembly.active_users, StateMachine())
        Assembly.api = APIFactory.Make()

    @staticmethod
    def __PrintFormPrototypes():
        graph = Assembly.graph

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

