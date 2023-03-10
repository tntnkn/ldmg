from dotenv import load_dotenv
import os 


class Config():
    def __init__(self):
        dir_path = os.path.dirname(
            os.path.dirname(os.path.realpath(__file__)) )
        f_name   = os.path.join(dir_path, '.env')
        load_dotenv(dir_path + '/.env')

        self.API_TOKEN = os.getenv('API_TOKEN')

