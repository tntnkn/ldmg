from .Interface     import FormElem
from .StateHistory  import StateHistory
from .Exceptions    import FormElemSwitchedHistory


class RegularTextFormElem(FormElem):
    def __init__(self, field, group):
        super().__init__(field, group)
        self.type       = 'TEXT'

    def IsCompleted(self, context):
        return True


class RegularFieldFormElem(FormElem):
    def __init__(self, field, group):
        super().__init__(field, group)
        self.type       = 'FORM'
        
    def AcceptInput(self, input, context):
        if input['cb'] == '':
            self.Reject(context)
        else:
            super().AcceptInput(input, context)

    def ToDict(self, context):
        d = super().ToDict(context)
        t = context.user_input.Read(self.storage_id)
        if t is not None:
            d['text'] = t
        return d


class DynamicFieldFormElem(FormElem):
    SEPARATOR = ', '

    def __init__(self, field, group):
        super().__init__(field, group)
        self.type       = 'D_FORM_CHIEF'
        self.d_id       = None
        
    def AcceptInput(self, input, context):
        cb = None 
        if input['d_id'] is not None:
            cb = self.__InputToOldDField(input, context)
        else:
            cb = self.__InputToNewDField(input, context)

        if cb is None:
            super().Reject(context)
        else:
            input['cb'] = cb
            super().AcceptInput(input, context)
        
    def ToDict(self, context):
        my_repr = super().ToDict(context)
        my_repr['d_id'] = None
        ret = list()
        ret.append(my_repr)
        d_fields_s = context.user_input.Read(self.storage_id)
        if d_fields_s is None: 
            return ret
        d_fields = d_fields_s.split(DynamicFieldFormElem.SEPARATOR)
        for cnt, d_field in enumerate(d_fields):
            ret.append( {
                'id'        : self.id,
                'd_id'      : cnt,
                'type'      : 'D_FORM',
                'cb'        : self.cb,
                'text'      : d_field,
                'completed' : True,
            } )
        return ret

    def AddRepr(self, where, context):
        where.extend( self.ToDict(context) )

    def __InputToOldDField(self, input, context):
        d_fields = context.user_input.Read(self.storage_id).split(
            DynamicFieldFormElem.SEPARATOR)
        if input['d_id'] > len(d_fields)-1:
            raise 'Dynamic field is not present!'
        if input['cb'] == '':
            d_fields.pop( input['d_id'] )
        else:
            d_fields[ input['d_id'] ] = input['cb']
        print(" OLD D_FIELDS ARE ", d_fields)
        if len(d_fields) == 0:
            return None
        return DynamicFieldFormElem.SEPARATOR.join(d_fields)

    def __InputToNewDField(self, input, context):
        if input['cb'] == '':
            return
        d_fields_s = context.user_input.Read(self.storage_id) 
        if d_fields_s is None:
            d_fields_s = input['cb']
        else:
            d_fields_s += DynamicFieldFormElem.SEPARATOR + input['cb']
        print(" NEW D_FIELDS ARE ", d_fields_s)
        return d_fields_s         


class ButtonFormElem(FormElem):
    def __init__(self, field, group):
        super().__init__(field, group)
        self.type       = 'BUTTON'

    def AcceptInput(self, input, context):

        super().AcceptInput(input, context)
        next_id = self.FormElemToNext(context)
        StateHistory.SetNext(next_id, context)
        StateHistory.SwitchToNext(context)
        raise FormElemSwitchedHistory(self.text) 
    

class SingleChoiceFormElem(FormElem):
    def __init__(self, field, group):
        super().__init__(field, group)
        self.type       = 'S_CHOICE'

    def AcceptInput(self, input, context):
        if self.IsCompleted(context):
            self.Reject(context)
        for groupee in self.group:
            groupee.Reject(context)
        return super().AcceptInput(input, context)


class MultiChoiceFormElem(FormElem):
    def __init__(self, field, group):
        super().__init__(field, group)
        self.type       = 'M_CHOICE'

    def AcceptInput(self, input, context):
        if self.IsCompleted():
            self.Reject(context)
        return super().AcceptInput(input, context)

