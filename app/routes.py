from flask import Blueprint, render_template, redirect, url_for, flash, request
from app import db, bcrypt
from app.models import User, Product
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
    products = Product.query.all()
    return render_template("home.html", title="Home", user=current_user, products=products)

@main.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data).first():
            flash("This email is already registered. Please log in or use another email.", "danger")
            return redirect(url_for("main.register"))

        if User.query.filter_by(username=form.username.data).first():
            flash("This username is already taken. Please choose another one.", "danger")
            return redirect(url_for("main.register"))

        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user = User(username=form.username.data, email=form.email.data, password=hashed_password, is_admin=False)
        db.session.add(user)
        db.session.commit()

        flash("Your account has been created! You can now log in.", "success")
        return redirect(url_for("main.login"))
    elif form.errors:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"{form[field].label.text}: {error}", "danger")

    return render_template("register.html", title="Register", form=form)

@main.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()

        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash(f"Welcome, {user.username}!", "success")
            next_page = request.args.get("next")
            return redirect(next_page) if next_page else redirect(url_for("main.dashboard"))
        else:
            flash("Login unsuccessful. Please check your email and password.", "danger")
    elif form.errors:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"{form[field].label.text}: {error}", "danger")

    return render_template("login.html", title="Login", form=form)

@main.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("main.login"))

@main.route("/about")
def about():
    return render_template("about.html", title="About")
