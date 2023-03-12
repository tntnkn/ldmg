from ..bot import bot
from aiogram.types import ParseMode 


class MessageManager():
    @staticmethod
    async def SendText(text, tg_user_id):
        resp = await bot.send_message(
                 tg_user_id, 
                 text,
                 parse_mode=ParseMode.HTML)
        return resp.message_id

    @staticmethod
    async def SendInlineKB(kb, kb_desc, tg_user_id):
        resp = await bot.send_message(
                 tg_user_id, 
                 kb_desc,
                 reply_markup=kb,
                 parse_mode=ParseMode.HTML)
        return resp.message_id

    @staticmethod
    async def Delete(message_id, tg_user_id):
        return await bot.delete_message(tg_user_id, message_id)

    @staticmethod
    async def SendDocument(document, tg_user_id):
        return await bot.send_document(
                chat_id=tg_user_id, 
                document=document)


class Send():
    @staticmethod
    async def NoTextInputWarning(tg_user_id):
        return await MessageManager.SendText(
                'Сейчас нельзя ничего написать.\nЕсли Вы ещё не начинали работу, то нажмите /start.', 
                tg_user_id)

    @staticmethod
    async def NoButtonPressWarning(tg_user_id):
        return await MessageManager.SendText(
                'Сейчас нельзя нажимать на кнопки.\nЕсли Вы ещё не начинали работу, то нажмите /start.', 
                tg_user_id)

    @staticmethod
    async def PromptForInput(tg_user_id):
        return await MessageManager.SendText(
                'Введите данные:', 
                tg_user_id)

    @staticmethod
    async def NoCommandsInputWarning(tg_user_id):
        return await MessageManager.SendText(
                'Прежде всего нажмите /start', 
                tg_user_id)

    @staticmethod
    async def TooLongInput(tg_user_id):
        return await MessageManager.SendText(
                'Ввод получился слишком длинным, попробуйте покороче:', 
                tg_user_id)

