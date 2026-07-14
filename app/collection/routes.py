from flask import render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user

from .service import collection_service
from .. import db
from ..models import Collection
from . import collection
from ..activity.service import activity_service
from ..search import pagination
from ..search.filters import SearchFilters
from ..search.service import search_service


@collection.route("/add/<card_id>", methods=["POST"])
@login_required
def add_card(card_id: str):

    collection_service.add_card_to_collection(current_user, card_id)

    flash("Card added to collection!", "success")

    if request.referrer:
        return redirect(request.referrer)

    return redirect(url_for("cards.card_detail", card_id=card_id))


@collection.route("/remove/<card_id>", methods=["POST"])
@login_required
def remove_card(card_id: str):

    result = collection_service.remove_card_from_collection(
        current_user,
        card_id
    )

    if result is None:
        flash("Card not found in your collection.", "warning")

        return redirect(url_for("collection.my_collection"))

    if result:
        flash("Card removed from your collection.", "success")

    else:
        flash("One copy removed from your collection.", "success")

    return redirect(url_for("collection.my_collection"))


@collection.route("/my_collection", methods=["GET"])
@login_required
def my_collection():
    filters = SearchFilters(request.args)

    context = search_service.get_search_context()

    cards = collection_service.get_collection(current_user, filters)

    return render_template(
        "collection/index.html",
        cards=cards,
        pagination=cards.pagination,
        filters=filters,
        **context
    )
