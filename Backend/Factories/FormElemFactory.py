from ..FormElems    import *
from ..Interface    import FormElem
from ..Types        import FormType
from ..Exceptions   import UnsupportedFormElemType
from typing         import List


class FormElemFactory():
    prev_field_type   = None
    current_group: List[FormElem] = list()

    def Make(graph_field) -> FormElem:
        if graph_field['type']!=FormElemFactory.prev_field_type:
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
            case _:
                raise UnsupportedFormElemType(\
                    graph_field['type'].value)

