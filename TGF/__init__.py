from aiogram    import executor
from .bot       import dp
from .Factories import BackAPIFactory, DocumentFactory
from .Storage   import Storage
from .Utils     import CommandsManager


def start_bot(back_api):
    BackAPIFactory.INIT(back_api)
    back_info = back_api.RegisterFrontendAPI(None)
    Storage().SetBackInfo(back_info)

    CommandsManager.SetCommands()

    import TGF.handlers
    executor.start_polling(dp, skip_updates=True)


def register_docgen(docgen):
    DocumentFactory.INIT(docgen)

