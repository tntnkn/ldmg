from flask_login    import LoginManager, current_user, login_required
from flask_bcrypt   import Bcrypt
from .Interface     import UserAuth 
from .Utils         import require_login


login_manager = LoginManager()
login_manager.login_view = 'login'
bcrypt        = Bcrypt()

@login_manager.user_loader
def load_user(user_id):
    return UserAuth(user_id)

def init_auth(app):
    login_manager.init_app(app)
    bcrypt.init_app(app)
    UserAuth.lm = login_manager
    UserAuth.bc = bcrypt
    return app

