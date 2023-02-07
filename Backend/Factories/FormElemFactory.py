from ..FormElems    import *
from ..Types        import FormType


class FormElemFactory():
    prev_field_type   = None
    current_group     = list()

    def Make(graph_field):
        if graph_field['type'].value!=FormElemFactory.prev_field_type:
            FormElemFactory.prev_field_type = graph_field['type']    
            FormElemFactory.current_group   = list()

        g = FormElemFactory.current_group
        match graph_field['type'].value:
            case FormType.REGULAR_TEXT:
                return RegularTextFormElem(graph_field, g)
            case FormType.REGULAR_FIELD:
                return RegularFieldFormElem(graph_field, g)
            case FormType.DYNAMIC_FIELD:
                return DynamicFieldFormElem(graph_field, g)
            case FormType.BUTTON:
                return ButtonFormElem(graph_field, g)
            case FormType.SINGLE_CHOICE:
                return SingleChoiceFormElem(graph_field, g)
            case FormType.MULTI_CHOICE:
                return MultiChoiceFormElem(graph_field, g)
            case FormType.DOCUMENT:
                return DocumentFormElem(graph_field, g)
            case _:
                raise 'Cannot make form, unsupported type!'

