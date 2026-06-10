from flask import render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user
from . import main
from .forms import EditProfileForm
from .. import db


@main.route("/")
def index():
    return render_template("main/index.html")


@main.route("/profile")
@login_required
def profile():
    return render_template("main/profile.html")


@main.route("/profile/edit", methods=["GET", "POST"])
@login_required
def edit_profile():
    form = EditProfileForm(
        original_username=current_user.username,
        original_email=current_user.email
    )

    if request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email

    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data

        db.session.commit()

        flash("Your profile has been updated.")

        return redirect(url_for("main.profile"))

    return render_template("main/edit_profile.html", form=form)