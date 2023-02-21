class BackAPIFactory():
    api = None

    def INIT(back_api):
        BackAPIFactory.api = back_api

    def Make(): 
        if not BackAPIFactory.api:
            raise RuntimeError('Back API is not inited')
        return BackAPIFactory.api

