from flask import flash, redirect, url_for, render_template
from . import auth
from sqlalchemy import or_
from .forms import RegistrationForm, LoginForm
from flask_login import login_user, login_required, logout_user
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

        flash("Registration successful. You can now log in.")

        return redirect(url_for("auth.login"))

    return render_template("auth/register.html", form=form)


@auth.route("/login", methods=["GET", "POST"])
def login():
    form: LoginForm = LoginForm()

    if form.validate_on_submit():
        user: User = User.query.filter(
            or_(
                User.username == form.identifier.data,
                User.email == form.identifier.data
            )
        ).first()

        if user is not None and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)

            flash("Logged in successfully.")

            return redirect(url_for("main.dashboard"))

        flash("Invalid username/email or password.")

    return render_template("auth/login.html", form=form)


@auth.route("/logout")
@login_required
def logout():
    logout_user()

    flash("You have been logged out.")

    return redirect(url_for("main.index"))
