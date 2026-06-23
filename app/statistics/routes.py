from flask import render_template
from flask_login import login_required, current_user
from . import statistics
from .services import get_user_statistics

@statistics.route("/", methods=["GET"])
@login_required
def index():
    stats = get_user_statistics(current_user)

    return render_template(
        "statistics/index.html",
        **stats
    )
