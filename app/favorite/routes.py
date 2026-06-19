from flask import flash, request, redirect, url_for, render_template
from flask_login import login_required, current_user
from . import favorite
from ..models import Favorite
from ..extensions import db
from ..cards.services import get_card


@favorite.route("/toggle/<card_id>", methods=["POST"])
@login_required
def toggle_favorite(card_id: str):
    favorite_card = Favorite.query.filter_by(
        user_id=current_user.id,
        card_id=card_id
    ).first()

    if favorite_card:
        db.session.delete(favorite_card)

        flash("You've removed this card from your favorites!", "success")

    else:
        favorite_card = Favorite(
            user_id=current_user.id,
            card_id=card_id
        )

        db.session.add(favorite_card)

        flash("Card added to favorites!", "success")

    db.session.commit()

    if request.referrer:
        return redirect(request.referrer)

    return redirect(url_for("cards.card_detail", card_id=card_id))


@favorite.route("/favorite_cards", methods=["GET"])
@login_required
def favorite_cards():
    favorites = []

    for favorite in current_user.favorites:
        favorites.append({
            "card": get_card(favorite.card_id)
        })

    return render_template("favorite/index.html", favorites=favorites)
