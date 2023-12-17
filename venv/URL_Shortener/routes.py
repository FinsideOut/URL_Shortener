from flask import render_template, redirect, flash, request
from URL_Shortener import app, db, bcrypt
from URL_Shortener.models import URL
from URL_Shortener.forms import URL_Form, Login_Form, Register_Form
from URL_Shortener.utils import ask_gpt, shorten_url


@app.route("/",methods = ["GET", "POST"])
def home():
    url_form = URL_Form()
    login_form = Login_Form()
    register_form = Register_Form()
    if url_form.validate_on_submit():
        if url_form.check_allias():
            short_url = shorten_url(url_form.allias.data)
            new_URL = URL(long_URL = url_form.long_URL.data, allias = url_form.allias.data, short_URL = short_url)
            db.session.add(new_URL)
            db.session.commit()
            quote,author = ask_gpt(url_form.allias.data)
            #quote = "Test quote"
            #author = "Me"
            #flash(f"{quote} - {author}", "success")
            return render_template("index.html", title = "Home", url_form = url_form, login_form = login_form, register_form = register_form, short_url = short_url, quote = quote, author = author)
    # if login_form.validate_on_submit():
    #     return render_template("index.html", title = "Home", url_form = url_form, login_form = login_form, register_form = register_form, short_url = short_url, quote = quote, author = author)
        

    return render_template("index.html", title = "Home", url_form = url_form, login_form = login_form,register_form = register_form)

@app.route("/<string:allias>")
def temp_url(allias):
    url = URL.query.filter_by(allias = allias).first()
    return redirect(url.long_URL)
