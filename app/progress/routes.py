from flask import render_template
from flask_login import login_required, current_user
from . import progress
from ..collection.service import collection_service


@progress.route("/")
@login_required
def index():
    sets = collection_service.get_collection_progress(current_user)

    return render_template("progress/index.html", sets=sets)
