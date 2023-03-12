from .forms     import (RegisterUserForm, LoginUserForm, 
                        RequestResetPasswordForm, ResetPasswordForm, 
                        AddGraphCredentialsForm)


def init_forms(app):
    app.config['WTF_CSRF_SECRET_KEY'] = app.config['SECRET_KEY']
    return app

