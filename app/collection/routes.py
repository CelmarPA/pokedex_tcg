from flask import render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user
from .. import db
from ..models import Collection
from . import collection
from ..cards.services import get_card_smart
from ..activity.services import log_activity


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
    search = request.args.get("search", "").strip().lower()

    cards = []

    for item in current_user.collections:

        card_data = get_card_smart(item.card_id)

        if not card_data:
            continue

        if search:
            name = card_data.get("name", "").lower()

            if search not in name:
                continue

        cards.append({
            "card": card_data,
            "quantity": item.quantity
        })

    return render_template("collection/index.html", cards=cards, search=search)


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
