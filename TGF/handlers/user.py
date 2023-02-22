from ..Factories    import BackAPIFactory, FormFactory
from ..Storage      import UserStorageView
from ..Utils        import CallbackTransformer, AllowedInputTypeHelper, Send, MessagesArchive
from ..Static       import AllowedInputType
from ..bot          import dp, types


back_api = BackAPIFactory.Make()


# --- Commands Handlers

@dp.message_handler(commands=['start'])
async def startCommandHandler(message: types.Message):
    user_id = back_api.NewUser() 
    s_view  = UserStorageView(message.from_id)
    s_view.Write('back_id', user_id)

    MessagesArchive.Memo(message.message_id, message.from_id)

    allowed = s_view.Read('allowed_input_types')
    allowed = AllowedInputTypeHelper.AddAllowedInput(
            AllowedInputType.CB, allowed)
    s_view.Write('allowed_input_types', allowed)

    req = {
        'user_id'   : user_id,
        'type'      : 'input',
        'contents'  : None,
    }

    old_form = s_view.Read('displayed_form')
    if old_form:
        await old_form.Hide()
    resp = back_api.AcceptInput(req)
    form = FormFactory.Make(resp['contents'], message.from_id)
    await form.Display()
    s_view.Write('displayed_form', form)



# --- Text input handlers

@dp.message_handler()
async def generalTextMessageHandler(message: types.Message):
    tg_user_id  = message.from_id
    s_view      = UserStorageView(message.from_id)
    allowed     = s_view.Read('allowed_input_types')

    MessagesArchive.Memo(message.message_id, tg_user_id)

    if not AllowedInputTypeHelper.CheckIfInputIsAllowed(
            AllowedInputType.TEXT, allowed):
        id = await Send.NoTextInputWarning(tg_user_id)
        MessagesArchive.Memo(id, tg_user_id)
        return

    allowed = AllowedInputTypeHelper.DeleteAllowedInput(
            AllowedInputType.TEXT, allowed)
    s_view.Write('allowed_input_types', allowed)

    field_type, field_id, _, d_id = CallbackTransformer.Split(
        s_view.Read('compressed_back_data'))
    user_id = s_view.Read('back_id')
    print("MESSAGE TEXT IS", message.text)
    contents = {
        'field_type'  : field_type,
        'field_id'    : field_id,
        'cb'          : message.text,
        'd_id'        : d_id,
    }

    req = {
        'user_id'   : user_id,
        'type'      : 'input',
        'contents'  : contents,
    }

    old_form = s_view.Read('displayed_form')
    if old_form:
        await old_form.Hide()
    resp = back_api.AcceptInput(req)
    form = FormFactory.Make(resp['contents'], tg_user_id)
    await form.Display()
    s_view.Write('displayed_form', form)


# --- Callback Query Handlers

@dp.callback_query_handler() 
async def generalCallbackQueryHandler(callback: types.CallbackQuery):
    await callback.answer()

    tg_user_id = callback['from']['id']
    s_view  = UserStorageView(tg_user_id)
    allowed = s_view.Read('allowed_input_types')

    if not AllowedInputTypeHelper.CheckIfInputIsAllowed(
            AllowedInputType.CB, allowed):
        id = await Send.NoButtonPressWarning(tg_user_id)
        MessagesArchive.Memo(id, tg_user_id)
        return

    field_type, field_id, cb, _ = \
        CallbackTransformer.Split(callback.data)

    if field_type == 'FORM' or field_type == 'D_FORM':
        allowed = AllowedInputTypeHelper.AddAllowedInput(
                AllowedInputType.TEXT, allowed)
        s_view.Write('allowed_input_types', allowed)
        s_view.Write('compressed_back_data', callback.data)
        id = await Send.PromptForInput(tg_user_id)
        MessagesArchive.Memo(id, tg_user_id)
        return

    allowed = AllowedInputTypeHelper.DeleteAllowedInput(
            AllowedInputType.TEXT, allowed)
    s_view.Write('allowed_input_types', allowed)
        
    user_id = s_view.Read('back_id')

    contents = {
        'field_type'  : field_type,
        'field_id'    : field_id,
        'cb'          : cb,
    }

    req = {
        'user_id'   : user_id,
        'type'      : 'input',
        'contents'  : contents,
    }

    old_form = s_view.Read('displayed_form')
    if old_form:
        await old_form.Hide()
    resp = back_api.AcceptInput(req)
    form = FormFactory.Make(resp['contents'], tg_user_id)
    await form.Display()
    s_view.Write('displayed_form', form)
