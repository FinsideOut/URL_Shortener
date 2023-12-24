from flask import render_template, redirect, request, jsonify, url_for, Blueprint
from URL_Shortener import app, db, bcrypt
from URL_Shortener.models import URL
from URL_Shortener.links.forms import URL_Form
from flask_login import current_user, login_required
from datetime import datetime, timedelta
from URL_Shortener.utils import ask_gpt, shorten_url, get_examples


from URL_Shortener.utils import build_logger
logger = build_logger()

links = Blueprint("links", __name__)



@links.route('/url_submit', methods=['POST'])
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

@links.route("/<string:allias>")
def temp_url(allias):
    if allias:
        url = URL.query.filter_by(allias = allias).first()
        if url:
            if url.date_expired <= datetime.utcnow():
                url.active = False
                db.session.commit()
                if url.date_expired + timedelta(days = 7) <= datetime.utcnow():
                    db.session.delete(url)
            else:
                return redirect(url.long_URL)
    return render_template("404.html")

@links.route("/user_links")
@login_required
def user_links():
    #next line DOES work, but the datedatimes of all posts are the same!?
    urls = URL.query.filter_by(user_id = current_user.user_id).order_by(URL.date_expired.desc()).all()
    for url in urls:        
        if url.date_expired <= datetime.utcnow():
            url.active = False
        if url.date_expired + timedelta(days = 7) <= datetime.utcnow():
            db.session.delete(url)
            
    warning = False
    for url in urls:
        if url.active == False:
            warning = True
            break
    db.session.commit()
    return render_template("user-links.html", urls = urls, warning = warning)

@links.route("/deactivate/<string:id>")
@login_required
def deactivate(id):
    url = URL.query.get(id)
    if url:
        url.active = False
        url.date_expired = datetime.utcnow()
        db.session.commit()
    return redirect(url_for("links.user_links"))

@links.route("/reactivate/<string:id>")
@login_required
def reactivate(id):
    url = URL.query.get(id)
    if url:
        url.active = True
        url.date_expired = datetime.utcnow() + timedelta(days = 3)
        db.session.commit()
    return redirect(url_for("links.user_links"))

@links.route("/extend/<string:id>")
@login_required
def extend(id):
    url = URL.query.get(id)
    if url:
        url.date_expired += timedelta(days = 3)
        db.session.commit()
    return redirect(url_for("links.user_links"))

@links.route("/delete/<string:id>")
@login_required
def delete(id):
    logger.warning("deleting")
    url = URL.query.get(id)
    if url:
        db.session.delete(url)
        db.session.commit()
    return redirect(url_for("links.user_links"))