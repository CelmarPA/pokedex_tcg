from flask import flash, redirect, url_for, render_template
from . import auth
from .forms import RegistrationForm
from ..models import User
from .. import db


@auth.route("/register", methods=["GET", "POST"])
def register():
    form: RegistrationForm = RegistrationForm()

    if form.validate_on_submit():
        user: User = User(
            username=form.username.data,
            email=form.email.data
        )

        user.password = form.password.data

        db.session.add(user)
        db.session.commit()

        flash( "Registration successful. You can now log in.")

        return redirect(url_for("auth.login"))

    return render_template("auth/register.html", form=form)


@auth.route("/login", methods=["GET", "POST"])
def login():
    return "Login Page"