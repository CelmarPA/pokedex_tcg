# app/auth/forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo, ValidationError
from ..models import User


class RegistrationForm(FlaskForm):

    username = StringField("Username", validators=[DataRequired(), Length(3, 30),
                                                        Regexp(r"^[A-Za-z][A-Za-z0-9_-]*$",
                                                               message="Username must start with a letter and contain only letters, numbers, underscores or hyphens.")])
    email = StringField("Email", validators=[DataRequired(), Length(1, 64), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=8), EqualTo("password2",
                                                                                  message="Passwords must match.")])
    password2 = PasswordField("Confirm Password", validators=[DataRequired()])
    submit = SubmitField("Register")

    def validate_username(self, field: StringField) -> None:
        if User.query.filter_by(username=field.data).first():
            raise ValidationError("Username already in use.")

    def validate_email(self, field: StringField) -> None:
        if User.query.filter_by(email=field.data).first():
            raise ValidationError("Email already registered.")


class LoginForm(FlaskForm):

    identifier = StringField("Username or Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Keep me logged in")
    submit = SubmitField("Login")
