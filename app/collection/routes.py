from flask import render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user
from .. import db
from ..models import Collection
from . import collection
from ..cards.service import card_service
from ..activity.services import log_activity
from ..search.filters import SearchFilters
from ..search.service import get_search_context, match_search


@collection.route("/add/<card_id>", methods=["POST"])
@login_required
def add_card(card_id: str):

    card = Collection.query.filter_by(
        user_id=current_user.id,
        card_id=card_id
    ).first()

    if not card:
        card = Collection(
            user_id=current_user.id,
            card_id=card_id,
            quantity=1
        )

        db.session.add(card)

    else:
        card.quantity += 1

    log_activity(
        current_user.id,
        card_id,
        "collection_add"
    )

    db.session.commit()

    flash("Card added to collection!", "success")

    if request.referrer:
        return redirect(request.referrer)

    return redirect(url_for("cards.card_detail", card_id=card_id))


@collection.route("/my_collection", methods=["GET"])
@login_required
def my_collection():
    filters = SearchFilters(request.args)

    search = filters.search.casefold()

    context = get_search_context()

    cards = []

    for item in current_user.collections:

        card_data = card_service.get_card_smart(item.card_id)

        if not card_data:
            continue

        if not match_search(search, card_data.get("name", "")):
            continue

        cards.append({
            "card": card_data,
            "quantity": item.quantity
        })

    return render_template(
        "collection/index.html",
        cards=cards,
        filters=filters,
        **context
    )


@collection.route("/remove/<card_id>", methods=["POST"])
@login_required
def remove_card(card_id: str):

    card = Collection.query.filter_by(
        user_id=current_user.id,
        card_id=card_id
    ).first()

    if not card:
        flash("Card not found in your collection.", "warning")
        return redirect(url_for("collection.my_collection"))

    removed_last_copy = card.quantity == 1

    if removed_last_copy:
        db.session.delete(card)
    else:
        card.quantity -= 1

    log_activity(
        current_user.id,
        card_id,
        "collection_remove"
    )

    db.session.commit()

    if removed_last_copy:
        flash("Card removed from your collection.", "success")
    else:
        flash("One copy removed from your collection.", "success")

    return redirect(url_for("collection.my_collection"))
