from . import achievement
from flask import render_template
from flask_login import login_required, current_user
from .services import get_user_achievements_progress


@achievement.route("/")
@login_required
def index():

    achievements_progress = get_user_achievements_progress(current_user)

    return render_template(
        "achievements/index.html",
        **achievements_progress
    )
