class Form():
    def __init__(self):
        self.groups = list()

    def AddGroup(self, group):
        if not group:
            return
        self.groups.append(group)

    async def Display(self, tg_user_id):
        for group in self.groups:
            await group.Display(tg_user_id)

