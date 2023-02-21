from aiogram.types  import InlineKeyboardMarkup, InlineKeyboardButton
from ..Utils        import CallbackTransformer


class FormElemGroup():
    def __init__(self):
        pass

    def AddElem(self, elem):
        raise NotImplementedError

    def Display(self, tg_user_id):
        raise NotImplementedError
      

class TextMessage(FormElemGroup):
    def __init__(self):
        self.type  = 'TEXT'
        self.texts = list()

    def AddElem(self, elem):
        self.texts.append(elem['text'])

    async def Display(self, tg_user_id):
        for text in self.texts:
            await MessageSender.SendText(text, tg_user_id)


class InlineKeyboard(FormElemGroup):
    def __init__(self):
        self.type = None
        self.kb   = InlineKeyboardMarkup(
                    row_width=2, 
                    resize_keyboard=True)
        self.kb_desc = None

    def AddElem(self, elem):
        if   not self.type:
            self.__AddType(elem)
        elif self.type != elem['type']:
            raise 'Wrong element type for Inline Keyboard'
        self.kb.add(
            InlineKeyboardButton(
                text=elem['text'], 
                callback_data=CallbackTransformer.Join(
                    elem['type'], elem['id'], elem['cb'])))

    async def Display(self, tg_user_id):
        await MessageSender.SendInlineKB(self.kb, 
                                         self.kb_desc,
                                         tg_user_id)

    def __AddType(self, elem):
        self.type = elem['type']
        match(elem['type']):
            case 'FORM':
                self.kb_desc = 'Заполните форму:'
            case 'D_FORM':
                self.kb_desc = 'Добавьте несколько вариантов:'
            case 'BUTTON':
                self.kb_desc = 'Выберете один из вариантов:'
            case 'S_CHOICE':
                self.kb_desc = 'Выберете один из вариантов:'
            case 'M_CHOICE':
                self.kb_desc = 'Выберете несколько из вариантов:'



from ..bot import bot
from aiogram.types import ParseMode 

class MessageSender():
    @staticmethod
    async def SendText(text, tg_user_id):
        await bot.send_message(tg_user_id, 
                         text,
                         parse_mode=ParseMode.HTML)

    @staticmethod
    async def SendInlineKB(kb, kb_desc, tg_user_id):
        await bot.send_message(tg_user_id, 
                         kb_desc,
                         reply_markup=kb,
                         parse_mode=ParseMode.HTML)


