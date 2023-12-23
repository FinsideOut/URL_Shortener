from flask import render_template, redirect, request, jsonify, url_for, Blueprint
from URL_Shortener import app, db, bcrypt
from URL_Shortener.models import User
from URL_Shortener.users.forms import Login_Form, Register_Form
from flask_login import login_user, logout_user, current_user, login_required
from URL_Shortener.utils import build_logger

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
    return render_template("user-links.html")