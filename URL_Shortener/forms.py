from flask_wtf import FlaskForm,RecaptchaField
from wtforms import StringField, SubmitField, PasswordField, BooleanField, validators
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from wtforms.validators import URL as URL_Validator
from URL_Shortener.models import URL, User
from URL_Shortener import app, db, bcrypt
from flask_login import current_user

    
# Functions named 'validate_(something)' are called automatically when 'validate_on_submit() is called
   
class URL_Form(FlaskForm):
    long_URL = StringField("Enter Long URL", validators = [DataRequired(), URL_Validator()])
    allias = StringField("Enter Allias", validators = [DataRequired(), Length(min = 1, max = 20)])
    recaptcha = RecaptchaField()
    submit = SubmitField("Get URL")

    def validate_allias(self, field):
        allias = URL.query.filter_by(allias = field.data).first()
        if allias:
            raise ValidationError("This allias already exists")
        
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
        print(user)
        if user:
            password = bcrypt.check_password_hash(user.password, field.data)
            print(password)
            if not password:
                raise ValidationError('Password Incorrect')
    


