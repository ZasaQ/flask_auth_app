from flask_wtf import FlaskForm
from flask import jsonify
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models import User

class RegistrationForm(FlaskForm):
    username = StringField(
        "Username",
        validators=[DataRequired(), Length(min=5, max=20, message="Username must be between 5 and 20 characters.")],
    )
    email = StringField(
        "Email",
        validators=[DataRequired(), Email(message="Enter a valid email address.")],
    )
    password = PasswordField(
        "Password",
        validators=[DataRequired(), Length(min=6, message="Password must be at least 6 characters.")],
    )
    confirm_password = PasswordField(
        "Confirm Password",
        validators=[DataRequired(), EqualTo('password', message="Passwords must match.")],
    )
    submit = SubmitField("Sign Up")

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email("Enter a valid email address.")])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField("Login")