from flask_login    import login_required


def require_login(route):
    return login_required(route) 

