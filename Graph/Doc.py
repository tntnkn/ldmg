from typing     import TypedDict, List, Dict, Union
from enum       import Enum, unique

from .Types     import ID_TYPE


class Doc(TypedDict, total=True):
    id              : ID_TYPE
    name            : str
    tag             : str


def get_dummy_doc() -> Doc:
    return {
        'id'            : '',
        'name'          : 'dummy',
        'tag'           : '',
    }


if __name__ == '__main__':
    doc : Doc = get_dummy_doc()
    print(doc)

