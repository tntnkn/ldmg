class Form():
    def __init__(self, tg_user_id):
        self.tg_user_id = tg_user_id
        self.groups     = list()

    def AddGroup(self, group):
        if not group:
            return
        self.groups.append(group)

    async def Display(self):
        for group in self.groups:
            await group.Display()

    async def Hide(self):
        for group in self.groups:
            await group.Hide()

