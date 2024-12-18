from flask import Blueprint, render_template, redirect, url_for, flash, request
from app import db, bcrypt
from app.models import User
from app.forms import RegistrationForm, LoginForm
from flask_login import login_user, logout_user, current_user, login_required

main = Blueprint("main", __name__)

@main.route("/")
def home():
    if not current_user.is_authenticated:
        return redirect(url_for("main.login"))
    return redirect(url_for("main.dashboard"))

@main.route("/home")
@login_required
def dashboard():
    return render_template("home.html", title="Home")

@main.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash("Your account has been created! You can now log in.", "success")
        return redirect(url_for("main.login"))
    return render_template("register.html", title="Register", form=form)

@main.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=True)
            next_page = request.args.get("next")
            return redirect(next_page) if next_page else redirect(url_for("main.dashboard"))
        else:
            flash("Login Unsuccessful. Please check email and password.", "danger")
    return render_template('login.html', title="Login", form=form)

@main.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("main.login"))

@main.route("/about")
def about():
    return render_template("about.html", title="About")
