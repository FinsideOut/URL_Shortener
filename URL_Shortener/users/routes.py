from flask import render_template, redirect, request, jsonify, url_for, Blueprint
from URL_Shortener import app, db, bcrypt
from URL_Shortener.models import User,URL
from URL_Shortener.users.forms import Login_Form, Register_Form
from flask_login import login_user, logout_user, current_user, login_required
from URL_Shortener.utils import build_logger
from datetime import datetime, timedelta
logger = build_logger()

users = Blueprint("users", __name__)


# REGISTER NEW USER
@users.route('/register_submit', methods=['POST'])
def register_submit():
    form = Register_Form(request.form)
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        new_user = User(username = form.username.data, 
                        email = form.email.data,
                        password = hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return jsonify(success=True)
    else:
        # Return a response with errors if validation fails
        errors = {field.name: field.errors for field in form}
        return jsonify(success=False, errors=errors)

#LOGIN EXISTING USER
@users.route('/login_submit', methods=['POST'])
def login_submit():
    form = Login_Form(request.form)
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        login_user(user, remember = form.remember.data)
        logger.warning(f"{current_user.username} logged IN")

        return jsonify(success=True, username = user.username)
    else:
        # Return a response with errors if validation fails
        errors = {field.name: field.errors for field in form}
        return jsonify(success=False, errors=errors)

#LOGOUT EXISTING USER
@users.route("/logout")
@login_required
def logout():
    logger.warning(f"{current_user.username} logged OUT")
    logout_user()
    return redirect(url_for("main.home"))


@users.route("/user_links")
@login_required
def user_links():
    #next line DOES work, but the datedatimes of all posts are the same!?
    urls = URL.query.filter_by(user_id = current_user.user_id).order_by(URL.date_expired.desc()).all()
    for url in urls:           
        if url.date_expired <= datetime.utcnow():
            logger.info("URL UPDATED")
            url.active = False
    db.session.commit()
    return render_template("user-links.html", urls = urls)

@users.route("/deactivate/<string:id>")
@login_required
def deactivate(id):
    url = URL.query.get(id)
    if url:
        url.active = False
        url.date_expired = datetime.utcnow()
        db.session.commit()
    return redirect(url_for("users.user_links"))

@users.route("/reactivate/<string:id>")
@login_required
def reactivate(id):
    url = URL.query.get(id)
    if url:
        url.active = True
        url.date_expired = datetime.utcnow() + timedelta(days = 3)
        db.session.commit()
    return redirect(url_for("users.user_links"))

@users.route("/extend/<string:id>")
@login_required
def extend(id):
    url = URL.query.get(id)
    if url:
        url.date_expired += timedelta(days = 3)
        db.session.commit()
    return redirect(url_for("users.user_links"))

@users.route("/delete/<string:id>")
@login_required
def delete(id):
    logger.warning("deleting")
    url = URL.query.get(id)
    if url:
        db.session.delete(url)
        db.session.commit()
    return redirect(url_for("users.user_links"))