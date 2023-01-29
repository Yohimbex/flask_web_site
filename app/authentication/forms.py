from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, SubmitField, HiddenField, PasswordField
from wtforms.validators import DataRequired, Length


class RegisterForm(FlaskForm):
    id = HiddenField('id')
    name = StringField(
        'Your nickname',
        validators=[DataRequired(), Length(3, 100)],
        render_kw={'placeholder': 'Full name'}
    )
    email = EmailField(
        'Your email',
        validators=[DataRequired(), Length(10, 150)],
        render_kw={'placeholder': 'Email'}
    )
    password = PasswordField(
        'Your password',
        validators=[DataRequired(), Length(8, 100)],
        render_kw={'placeholder': 'Password'}
    )
    submit = SubmitField('Register')


class UserForm(FlaskForm):
    email = EmailField(
        'Your email',
        validators=[DataRequired(), Length(10, 150)],
        render_kw={'placeholder': 'Email'}
    )
    password = PasswordField(
        'Your password',
        validators=[DataRequired(), Length(8, 100)],
        render_kw={'placeholder': 'Password'}
    )
    login = SubmitField('Login')
