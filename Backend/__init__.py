from Backend.Factories  import Assembly


def get_api(loader):
    loader.load_graph()

    Assembly.Assemble(loader)
    return Assembly.api 

