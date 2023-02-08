class StorageView():
    def __init__(self, storage_part):
        self.storage = storage_part 

    def Read(self, key):
        return self.storage[key]

    def Write(self, key, value):
        self.storage[key] = value

    def Delete(self, key):
        self.storage[key] = None

    def Contains(self, key):
        return self.storage.get(key, None) is not None

    def TransactionGo(self):
        pass

class UserInputStorage(StorageView):
    def __init__(self, user_storage ):
        super().__init__(user_storage)


class UserContextStorage(StorageView):
    def __init__(self, user_context):
        super().__init__(user_context)


class GeneralInfoStorage(StorageView):
    def __init__(self, general_info):
        super().__init__(general_info)

    def Write(self, key, value):
        raise 'Operation "Write" is not supported!'

    def Delete(self, key):
        raise 'Operation "Delete" is not supported!'

class Context():
    def __init__(self, user_input, user_context, general_info):
        self.user_input     = user_input
        self.user_context   = user_context
        self.general_info   = general_info

