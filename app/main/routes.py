from flask import render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user
from . import main
from .forms import EditProfileForm
from .. import db
from ..statistics.services import get_user_statistics
from ..models import Activity
from ..cards.services import get_card_smart
from ..statistics.services import get_collection_progress, get_favorite_types, get_collection_rarity


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


@main.route("/dashboard")
@login_required
def dashboard():

    stats = get_user_statistics(current_user)

    collection_progress = get_collection_progress(current_user)[:6]

    favorite_types = get_favorite_types(current_user)

    collection_rarity = get_collection_rarity(current_user)

    recent_activities = Activity.query.filter_by(
        user_id=current_user.id
    ).order_by(
        Activity.created_at.desc()
    ).limit(10).all()

    activities = []

    for activity in recent_activities:
        card = get_card_smart(activity.card_id)

        activities.append({
            "action": activity.action,
            "card_name": card["name"],
            "created-at": activity.created_at
        })

    type_labels = [item["type"] for item in favorite_types]
    type_values = [item["count"] for item in favorite_types]

    rarity_labels = [item["rarity"] for item in collection_rarity]
    rarity_values = [item["count"] for item in collection_rarity]


    return render_template(
        "main/dashboard.html",
        recent_activities=activities,
        **stats,
        collection_progress=collection_progress,
        favorite_types=favorite_types,
        collection_rarity=collection_rarity,
        type_labels=type_labels,
        type_values=type_values,
        rarity_labels=rarity_labels,
        rarity_values=rarity_values
    )
