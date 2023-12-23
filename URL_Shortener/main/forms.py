from flask_wtf import FlaskForm,RecaptchaField
from wtforms import StringField, SubmitField, validators
from wtforms.validators import DataRequired, Length, ValidationError
from wtforms.validators import URL as URL_Validator
from URL_Shortener.models import URL


    
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
        



