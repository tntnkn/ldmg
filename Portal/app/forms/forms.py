from flask_wtf          import FlaskForm
from wtforms            import (StringField, EmailField, PasswordField, 
                                SubmitField)
from wtforms.validators import InputRequired, Length, Email, EqualTo

class RegisterUserForm(FlaskForm):
    name    = StringField(
                    'Имя', 
                    validators=[InputRequired(),
                                Length(min=4, max=30),]
            )
    email   = EmailField(
                    'Электронная почта',
                    validators=[InputRequired(),
                                Email(),]
            )
    password= PasswordField(
                    'Пароль',
                    validators=[InputRequired(),] 
            )
    confirm = PasswordField(
                    'Пароль ещё раз',
                    validators=[InputRequired(),
                                EqualTo('password'),] 
            )
    submit  = SubmitField(
                    'Отправить',
            )


class LoginUserForm(FlaskForm):
    email   = EmailField(
                    'Электронная почта',
                    validators=[InputRequired(),
                                Email(),]
            )
    password= PasswordField(
                    'Пароль',
                    validators=[InputRequired(),] 
            )
    submit  = SubmitField(
                    'Отправить',
            )


class RequestResetPasswordForm(FlaskForm):
    email   = EmailField(
                    'Электронная почта',
                    validators=[InputRequired(),
                                Email(),]
            )
    submit  = SubmitField(
                    'Отправить',
            )


class ResetPasswordForm(FlaskForm):
    email   = EmailField(
                    'Электронная почта',
                    validators=[InputRequired(),
                                Email(),]
            )
    password= PasswordField(
                    'Пароль',
                    validators=[InputRequired(),] 
            )
    confirm = PasswordField(
                    'Пароль ещё раз',
                    validators=[InputRequired(),
                                EqualTo('password'),] 
            )
    submit  = SubmitField(
                    'Отправить',
            )


class AddGraphCredentialsForm(FlaskForm):
    name         = StringField(
                    'Название', 
                    validators=[InputRequired(),
                                Length(min=4, max=30),]
            )
    user_email   = StringField(
                    'Почта пользователя', 
                    validators=[InputRequired(),
                                Email(),]
            )
    airtable_api_key = StringField(
        'airtable_api_key', validators=[InputRequired(),])
    airtable_base_id = StringField(
        'airtable_base_id', validators=[InputRequired(),])
    airtable_states_table_id = StringField(
        'airtable_states_table_id', validators=[InputRequired(),])
    airtable_states_table_view_id = StringField(
        'airtable_states_table_view_id', validators=[InputRequired(),])
    airtable_transitions_table_id = StringField( 
        'airtable_transitions_table_id', validators=[InputRequired(),])
    airtable_transition_table_view_id = StringField( 
        'airtable_transition_table_view_id', validators=[InputRequired(),])
    airtable_forms_table_id = StringField(
        'airtable_forms_table_id', validators=[InputRequired(),])
    airtable_forms_table_view_id = StringField( 
        'airtable_forms_table_view_id', validators=[InputRequired(),])
    airtable_config_table_id = StringField( 
        'airtable_config_table_id', validators=[InputRequired(),])
    airtable_config_table_view_id = StringField( 
        'airtable_config_table_view_id', validators=[InputRequired(),])

    submit  = SubmitField(
                    'Отправить',
            )
