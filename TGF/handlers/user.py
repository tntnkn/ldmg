from ..Factories    import BackAPIFactory, FormFactory
from ..Storage      import UserStorageView
from ..Utils        import CallbackTransformer
from ..bot          import dp, types


back_api = BackAPIFactory.Make()


# --- Commands Handlers

@dp.message_handler(commands=['start'])
async def startCommandHandler(message: types.Message):
    user_id = back_api.NewUser() 
    s_view  = UserStorageView(message.from_id)
    s_view.Write('back_id', user_id)

    req = {
        'user_id'   : user_id,
        'type'      : 'input',
        'contents'  : None,
    }

    resp = back_api.AcceptInput(req)
    form = FormFactory.Make(resp['contents'])
    await form.Display(message.from_id)


# --- Text input handlers

@dp.message_handler()
async def generalTextMessageHandler(message: types.Message):
    tg_user_id = message.from_id
    user_id = storage_h.GetUserBackId(tg_user_id)

    req = {
        'user_id'   : user_id,
        'type'      : 'input',
        'contents'  : contents,
    }

    resp = back_api.AcceptInput(req)
    form = FormFactory.Make(resp['contents'])
    await form.Display(tg_user_id)


# --- Callback Query Handlers

@dp.callback_query_handler() 
async def generalCallbackQueryHandler(callback: types.CallbackQuery):
    await callback.answer()

    field_type, field_id, cb = CallbackTransformer.Split(callback.data)

    contents = {
        'field_type'  : field_type,
        'field_id'    : field_id,
        'cb'          : cb,
    }

    tg_user_id = callback['from']['id']
    s_view  = UserStorageView(tg_user_id)
    user_id = s_view.Read('back_id')

    req = {
        'user_id'   : user_id,
        'type'      : 'input',
        'contents'  : contents,
    }

    resp = back_api.AcceptInput(req)
    form = FormFactory.Make(resp['contents'])
    await form.Display(tg_user_id)

