from flask import render_template
from flask_login import login_required, current_user
from . import statistics
from .service import statistics_service


@statistics.route("/", methods=["GET"])
@login_required
def index():
    stats = statistics_service.get_user_statistics(current_user)

    return render_template(
        "statistics/index.html",
        stats=stats
    )
