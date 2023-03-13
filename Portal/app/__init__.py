from maxdmgloader import API 

from flask          import Flask
from .config        import Config
from .auth          import init_auth, require_login 
from .forms         import init_forms
from .storage       import init_storage
from .graph         import init_dash


def init_app():
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object( Config() )

    with app.app_context():

        init_dash(app)
        init_auth(app)    
        init_forms(app)
        init_storage(app)

        from .          import routes

        for f_name, f in app.view_functions.items():
            print(f_name)
            if 'graph' in f_name:
                app.view_functions[f_name] = require_login(f) 
    return app

