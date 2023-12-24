from flask_wtf import FlaskForm,RecaptchaField
from wtforms import StringField, SubmitField, SelectField, validators
from wtforms.validators import DataRequired, Length, ValidationError
from wtforms.validators import URL as URL_Validator
from URL_Shortener.models import URL


    
# Functions named 'validate_(something)' are called automatically when 'validate_on_submit() is called
   
class URL_Form(FlaskForm):
    long_URL = StringField("Long URL", validators = [DataRequired(), URL_Validator()])
    allias = StringField("Alias", validators = [DataRequired(), Length(min = 1, max = 20)])
    # recaptcha = RecaptchaField()
    submit = SubmitField("Get URL")
    choices = [(0, "0 Days (testing)"), (1, "1 Day"), (2, "2 Days"), (3, "3 Days"), (4, "More (Sign In)", {"class":"text-muted"})]
    life_span = SelectField("Valid Duration", choices=choices, default="3")

    def validate_allias(self, field):
        allias = URL.query.filter_by(allias = field.data).first()
        if allias:
            raise ValidationError("This allias already exists")
        



