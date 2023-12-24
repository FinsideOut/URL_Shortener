from flask import render_template, redirect, request, jsonify, url_for, Blueprint
from URL_Shortener import app, db
from URL_Shortener.models import URL
from URL_Shortener.users.forms import Login_Form, Register_Form
from URL_Shortener.main.forms import URL_Form
from URL_Shortener.utils import ask_gpt, shorten_url, get_examples
from flask_login import current_user, login_required
from URL_Shortener.utils import build_logger
from datetime import datetime, timedelta

logger = build_logger()

main = Blueprint("main", __name__)


@main.route("/",methods = ["GET", "POST"])
def home():
    register_form = Register_Form()
    login_form = Login_Form()
    url_form = URL_Form()
    long_example, allias_example = get_examples()
    quote, author = ask_gpt(allias_example)
    return render_template("index.html", title = "Home", url_form = url_form, login_form = login_form, register_form = register_form, quote = quote, author = author, long_example = "Example: " + long_example, allias_example = "Example: " + allias_example)


@main.route('/url_submit', methods=['POST'])
def url_submit():
    form = URL_Form(request.form)
    if form.validate_on_submit():
        short_url = shorten_url(form.allias.data)
        new_URL = URL(long_URL = form.long_URL.data, 
                      allias = form.allias.data, 
                      short_URL = short_url, 
                      date_expired = datetime.utcnow() + timedelta(days = int(form.life_span.data)))
        if current_user.is_authenticated:
            new_URL.user_id = current_user.user_id
        db.session.add(new_URL)
        db.session.commit()
        quote,author = ask_gpt(form.allias.data)
        return jsonify(success=True,
                        quote = quote, 
                        author = author,
                        result = f"127.0.0.1:5000/{form.allias.data}")
    else:
        # Return a response with errors if validation fails
        errors = {field.name: field.errors for field in form}
        return jsonify(success=False, errors=errors)



@main.route("/<string:allias>")
def temp_url(allias):
    if allias:
        url = URL.query.filter_by(allias = allias).first()
        if url:
            if url.date_expired <= datetime.utcnow():
                url.active = False
                db.session.commit()
            else:
                return redirect(url.long_URL)
    return render_template("404.html")


        

    