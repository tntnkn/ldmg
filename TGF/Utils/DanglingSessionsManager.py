import asyncio
from time           import time

from ..Storage      import UsersLoop


class DanglingSessionsManager():
    DANGLING_SESSIONS_CHECKUP_STRIDE   = 20 * 60
    MAX_ALLOWED_DANGLING_TIME          = 20 * 60

    @staticmethod
    def Start():
        loop = asyncio.get_event_loop()
        loop.create_task(
            DanglingSessionsManager.dangling_sessions_control_loop())

    @staticmethod
    async def dangling_sessions_control_loop():
        print('created dangling manager')
        while True:
            print('danging manager loop')
            await asyncio.sleep(
                DanglingSessionsManager.DANGLING_SESSIONS_CHECKUP_STRIDE)
            await DanglingSessionsManager().delete_dangling_sessions()

    @staticmethod
    async def delete_dangling_sessions():
        print("in delete_dangling_sessions()")
        now = time()
        print("now is: ", now)
        for s_view in UsersLoop():
            then = s_view.Read('last_action_time')
            print("last action is: ", then)
            if now - then > \
               DanglingSessionsManager.MAX_ALLOWED_DANGLING_TIME:
                s_view.Destroy()
                print("SESSION EXPIRED!")

