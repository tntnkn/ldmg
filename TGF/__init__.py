from aiogram    import executor
from .bot       import dp
from .Factories import BackAPIFactory, DocumentFactory
from .Storage   import Storage
from .Utils     import CommandsManager, DanglingSessionsManager


def start_bot(back_api):
    BackAPIFactory.INIT(back_api)
    back_info = back_api.RegisterFrontendAPI(None)
    Storage().SetBackInfo(back_info)

    CommandsManager.SetCommands()
    DanglingSessionsManager.Start()

    import TGF.middleware
    middleware.setup(bot.dp)

    import TGF.handlers
    executor.start_polling(dp, skip_updates=True)


def register_docgen(docgen):
    DocumentFactory.INIT(docgen)

