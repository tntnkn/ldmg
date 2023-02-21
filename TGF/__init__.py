from aiogram    import executor
from .bot       import dp
from .Factories import BackAPIFactory



def start_bot(back_api):
    BackAPIFactory.INIT(back_api)

    import TGF.handlers
    executor.start_polling(dp, skip_updates=True)

