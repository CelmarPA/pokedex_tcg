from flask import render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user
from .. import db
from ..models import Collection
from . import collection
from ..cards.services import get_card


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

    flash("Card added to collection!", "success")

    db.session.commit()

    if request.referrer:
        return redirect(request.referrer)

    return redirect(url_for("cards.card_detail", card_id=card_id))


@collection.route("/my_collection", methods=["GET"])
@login_required
def my_collection():

    cards = []

    for collection in current_user.collections:
        cards.append({
            "card": get_card(collection.card_id),
            "quantity": collection.quantity
        })

    return render_template("collection/index.html", cards=cards)


@collection.route("/remove/<card_id>", methods=["POST"])
@login_required
def remove_card(card_id: str):
    card = Collection.query.filter_by(
        user_id=current_user.id,
        card_id=card_id
    ).first()

    if not card:
        return redirect(url_for("collection.my_collection"))

    if card.quantity > 1:
        card.quantity -= 1

    else:
        db.session.delete(card)

    db.session.commit()

    return redirect(url_for("collection.my_collection"))