from Backend.Factories      import (FormPrototypeFactory, StorageFactory, 
                                    ActiveUsersFactory, APIFactory)
from Backend.StateMachine   import StateMachine 
from Backend.StateHistory   import StateHistory 


class Assembly():
    storage         = None
    active_users    = None
    api             = None

    graph           = None
    forms           = None
    docs            = None

    @staticmethod
    def Assemble(loader):
        graph = loader['graph']
        forms = loader['forms']
        docs  = loader['docs']
        Assembly.graph = graph
        Assembly.forms = forms
        Assembly.docs  = docs

        print("Building storage")
        StorageFactory.INIT(graph, forms, docs)
        Assembly.storage = StorageFactory.Make()
        print("Building active_users")
        ActiveUsersFactory.INIT(Assembly.storage)
        Assembly.active_users = ActiveUsersFactory.Make()

        print("Building forms factory")
        FormPrototypeFactory.INIT(
                graph.states, 
                forms,
                Assembly.storage) 
        Assembly.__PrintFormPrototypes()

        print("BEFORE STATEHOSTORY INIT")
        StateHistory.INIT(FormPrototypeFactory)

        print("Building API")
        APIFactory.INIT(Assembly.active_users, 
                        Assembly.storage.GetGeneralInfoStorage(),
                        Assembly.storage.GetFormsInfoStorage(),
                        StateMachine())
        Assembly.api = APIFactory.Make()

    @staticmethod
    def __PrintFormPrototypes():
        graph = Assembly.graph

        print('\nForms are:')
        for form in FormPrototypeFactory.prototypes.values():
            print('- ', graph.states[form.id]['name'], form.fields, '\n')
"""
        print('\nTesting prototype factory:')
        for form in FormPrototypeFactory.prototypes.values():
            copy = FormPrototypeFactory.Make(form.id)
            print('- ', form.id, copy.id)
        for form in FormPrototypeFactory.prototypes.values():
            copy = FormPrototypeFactory.Make(form.id)
            copy.id = 'LALALA'
            print('- ', form.id, copy.id)
"""

