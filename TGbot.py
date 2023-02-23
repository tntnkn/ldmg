from TGF            import start_bot, register_docgen
from Backend        import get_api
from Graph          import Loader
from Docgen         import Docgen


def main():
    register_docgen( Docgen() )
    start_bot( get_api( Loader() ) )


if __name__ == '__main__':
    main()

