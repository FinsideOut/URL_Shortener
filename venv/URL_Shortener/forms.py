from flask_wtf import FlaskForm,RecaptchaField
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from wtforms.validators import URL as URL_Validator
from URL_Shortener.models import URL, User
from flask_login import current_user

class URL_Form(FlaskForm):
    long_URL = StringField("Enter Long URL", validators = [DataRequired(), URL_Validator()])
    allias = StringField("Enter Allias", validators = [DataRequired(), Length(min = 1, max = 20)])
    recaptcha = RecaptchaField()
    submit = SubmitField("Get URL")

    def check_allias(self):
        allias = URL.query.filter_by(allias = self.allias.data).first()
        if allias:
            self.allias.errors.append("This Alias Already Exists :(")
        else:
            return True

class Register_Form(FlaskForm):
    username = StringField("Username", validators = [DataRequired(),Length(min = 2, max = 20)])
    email = StringField("Email", validators = [DataRequired(), Email()])
    password = PasswordField("Password", validators = [DataRequired()])
    confirm_password = PasswordField("Confirm Password", validators = [DataRequired(), EqualTo("password")])
    submit = SubmitField("Sign Up")

    def check_user_exists(self):
        user = User.query.filter_by(allias = self.email.data).first()
        if user:
            self.email.errors.append("An account already exists with this email")
        else:
            return True
        
class Login_Form(FlaskForm):
    username = StringField("Username", validators = [DataRequired(),Length(min = 2, max = 20)])
    email = StringField("Email", validators = [DataRequired(), Email()])
    password = PasswordField("Password", validators = [DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Log In")
