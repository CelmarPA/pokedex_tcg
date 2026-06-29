from . import achievement
from flask import render_template
from flask_login import login_required, current_user
from .services import get_user_achievements


@achievement.route("/")
@login_required
def index():

    achievements = get_user_achievements(current_user)

    unlocked = sum(achievement_["unlocked"] for achievement_ in achievements)

    total = len(achievements)

    progress = (unlocked / total * 100) if total else 0

    return render_template(
        "achievements/index.html",
        achievements=achievements,
        unlocked=unlocked,
        total=total,
        progress=progress
    )
