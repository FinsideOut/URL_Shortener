from flask import render_template, redirect, flash
from URL_Shortener import app, db
from URL_Shortener.models import URL
from URL_Shortener.forms import URL_Form
from URL_Shortener.utils import ask_gpt, shorten_url


@app.route("/",methods = ["GET", "POST"])
def home():
    form = URL_Form()
   # place_holder = URL.query.get_or_404(1)
    if form.validate_on_submit():
        if form.check_allias():
            short_url = shorten_url(form.allias.data)
            new_URL = URL(long_URL = form.long_URL.data, allias = form.allias.data, short_URL = short_url)
            db.session.add(new_URL)
            db.session.commit()
            #quote,author = ask_gpt(form.allias.data)
            quote = "Test quote"
            author = "Me"
            flash(f"{quote} - {author}", "success")
            return render_template("index.html", title = "Home", form = form, short_url = short_url)
    else:
        print(form.errors)
    return render_template("index.html", title = "Home", form = form)

@app.route("/<string:allias>")
def temp_url(allias):
    url = URL.query.filter_by(allias = allias).first()
    return redirect(url.long_URL)
