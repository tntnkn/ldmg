from TGF            import start_bot
from Backend        import get_api
from Graph          import Loader

def main():
    start_bot( get_api( Loader() ) )


if __name__ == '__main__':
    main()

