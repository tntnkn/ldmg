from .Interface     import Storage


storage = None

def init_storage(app):
    global storage
    storage = Storage(app)


