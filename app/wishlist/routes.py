from flask import redirect, url_for, flash, request, render_template
from flask_login import current_user, login_required
from . import wishlist
from ..extensions import db
from ..models import Wishlist
from ..cards.services import get_card


@wishlist.route("/toggle/<card_id>", methods=["POST"])
@login_required
def toggle_wishlist(card_id: str):

    wish_card = Wishlist.query.filter_by(
        user_id=current_user.id,
        card_id=card_id
    ).first()

    if wish_card:
        db.session.delete(wish_card)

        flash("You've removed this card from your wishlist!", "success")

    else:
        wish_card = Wishlist(
            user_id=current_user.id,
            card_id=card_id
        )

        db.session.add(wish_card)

        flash("Card added to wishlist!", "success")

    db.session.commit()

    if request.referrer:
        return redirect(request.referrer)

    return redirect(url_for("cards.card_detail", card_id=card_id))


@wishlist.route("/my_wishlist", methods=["GET"])
@login_required
def my_wishlist():
    cards_wishlist = []

    for card in current_user.wishlists:
        cards_wishlist.append({
            "card": get_card(card.card_id)
        })

    return render_template("wishlist/index.html", cards_wishlist=cards_wishlist)
