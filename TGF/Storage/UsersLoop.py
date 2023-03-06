from .  import Storage, UserStorageView


class UsersLoop():
    def __init__(self):
        self.ids = Storage().GetUsersIds()

    def __iter__(self):
        return UsersLoopIterator(self.ids)


class UsersLoopIterator():
    def __init__(self, ids):
        self.ids = ids
        self.idx = 0

    def __next__(self):
        try:
            ret = UserStorageView( self.ids[self.idx] ) 
        except:
            raise StopIteration
        self.idx += 1
        return ret

