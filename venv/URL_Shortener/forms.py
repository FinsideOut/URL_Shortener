from flask_wtf import FlaskForm,RecaptchaField
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length



class URL_Form(FlaskForm):
    long_URL = StringField("Enter Long URL", validators = [DataRequired(), Length(min = 1, max = 300)])

    allias = StringField("Enter Allias", validators = [DataRequired(), Length(min = 1, max = 20)])
    
    # recaptcha = RecaptchaField()

    submit = SubmitField("Get URL")
