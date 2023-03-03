from TGF            import start_bot, register_docgen
from Backend        import get_api
from Graph          import API as GAPI
from Docgen         import Docgen


def main():
    resp        = GAPI().Load()
    back_api    = get_api(resp) 
    docgen      = Docgen(resp['docs'])

    register_docgen( docgen )
    start_bot(back_api)


if __name__ == '__main__':
    main()

