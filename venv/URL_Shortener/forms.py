from flask_wtf import FlaskForm,RecaptchaField
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError
from wtforms.validators import URL as URL_Validator
from URL_Shortener.models import URL
#from URL_Shortener.models import URL

class URL_Form(FlaskForm):
    long_URL = StringField("Enter Long URL", validators = [DataRequired(), URL_Validator()])
    allias = StringField("Enter Allias", validators = [DataRequired(), Length(min = 1, max = 20)])
    recaptcha = RecaptchaField()
    submit = SubmitField("Get URL")

    def check_allias(self):
        print("TESTING",self.allias.data)
        allias = URL.query.filter_by(allias = self.allias.data).first()
        if allias:
            self.allias.errors.append("This Alias Already Exists :(")
            #raise ValidationError("Alias already exists :(")
        else:
            return True
