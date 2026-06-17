from flask import render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user
from .. import db
from ..models import Collection
from . import collection


@collection.route("/add/<card_id>", methods=["GET", "POST"])
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

    return redirect(url_for("cards.card_detail", card_id=card_id))
