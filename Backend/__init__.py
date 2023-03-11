from .Assembly  import Assembly


def get_api(load_info):
    Assembly.Assemble(load_info)
    return Assembly.api 

