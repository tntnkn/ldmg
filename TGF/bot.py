from aiogram    import Bot, Dispatcher, types
from .Config    import Config


config = Config()

bot = Bot( token=config.API_TOKEN)
dp  = Dispatcher(bot)

