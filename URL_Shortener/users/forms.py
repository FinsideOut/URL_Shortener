from flask_wtf import FlaskForm,RecaptchaField
from wtforms import StringField, SubmitField, PasswordField, BooleanField, validators
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from URL_Shortener.models import User
from URL_Shortener import bcrypt

class Register_Form(FlaskForm):
    username = StringField("Username", validators = [DataRequired(),Length(min = 2, max = 20)])
    email = StringField("Email", validators = [DataRequired(), Email()])
    password = PasswordField("Password", validators = [DataRequired()])
    confirm_password = PasswordField("Confirm Password", validators = [DataRequired(), EqualTo("password")])
    submit = SubmitField("Sign Up")

    def validate_email(self, field):
        if User.query.filter_by(email = field.data).first():
            raise ValidationError('There is already an account with this email')
    
    def validate_username(self, field):
        if User.query.filter_by(username = field.data).first():
            raise ValidationError('There is already an account with this username')


class Login_Form(FlaskForm):
    # username = StringField("Username", validators = [DataRequired(),Length(min = 2, max = 20)])
    email = StringField("Email", validators = [DataRequired(), Email()])
    password = PasswordField("Password", validators = [DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Log In")

    def validate_email(self, field):
        if not User.query.filter_by(email = field.data).first():
            raise ValidationError('There is no account with this email')
        
    def validate_password(self, field):
        user = User.query.filter_by(email = self.email.data).first()
        if user:
            password = bcrypt.check_password_hash(user.password, field.data)
            if not password:
                raise ValidationError('Password Incorrect')
    