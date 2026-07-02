from . import achievement
from flask import render_template
from flask_login import login_required, current_user
from .service import achievement_service


@achievement.route("/")
@login_required
def index():

    ach_progress = achievement_service.get_user_achievements_progress(current_user)

    return render_template(
        "achievements/index.html",
        ach_progress=ach_progress
    )
