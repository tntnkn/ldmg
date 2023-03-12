import os
from dotenv     import load_dotenv


class Config():
    def __init__(self):
        load_dotenv()

        self.SECRET_KEY = os.getenv('SECRET_KEY')
        self.DB_URI     = os.getenv('DB_URI')

        #TODO 
        #look into environ for ConfigType or smth. Use 'Dev' as default.
        #rewrite defaults in .env.
    
