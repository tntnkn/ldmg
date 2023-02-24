from TGF            import start_bot, register_docgen
from Backend        import get_api
from Graph          import Loader
from Docgen         import Docgen


def main():
    loader      = Loader()
    back_api    = get_api( loader ) 
    docgen      = Docgen(loader.docs)

    register_docgen( docgen )
    start_bot(back_api)


if __name__ == '__main__':
    main()

