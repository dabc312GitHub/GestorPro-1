from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField
from wtforms.fields.html5 import EmailField
from wtforms.validators import InputRequired, Length, EqualTo, email_validator,ValidationError
from models import User
from passlib.hash import pbkdf2_sha256

def invalid_credentials(form,field):
    username_entered= form.username.data
    password_entered= field.data

    user_object=User.query.filter_by(usuario=username_entered).first()
    if user_object is None:
        raise ValidationError("Usuario o contraseña incorrectos")
    elif not pbkdf2_sha256.verify(password_entered,user_object.contraseña):
        raise ValidationError("Usuario o contraseña incorrectos")

class RegistrationForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(message="Usuario requerido"), Length(min=4, max=25, message="Usuario debe contener entre 4 y 25 caracteres")])
    password = PasswordField('password', validators=[InputRequired(message="Contraseña requerida"), Length(min=4, max=25, message="Contraseña debe contener entre 4 y 25 caracteres")])
    email = EmailField('email', validators=[InputRequired(message="Correo requerido")])
    submit_button=SubmitField('Registrarse')

    def validate_username(self, username):
        user_object= User.query.filter_by(usuario=username.data).first()
        if user_object:
            raise ValidationError("Usuario ya existe")
    def validate_email(self,email):
        email_object=User.query.filter_by(email=email.data).first()
        if email_object:
            raise ValidationError("Correo ya existe")

class LoginForm(FlaskForm):
    username=StringField('username', validators=[InputRequired(message="Campo requerido")])
    password=PasswordField('password', validators=[InputRequired(message="Campo requerido"),invalid_credentials])

    submit_button=SubmitField('Login')