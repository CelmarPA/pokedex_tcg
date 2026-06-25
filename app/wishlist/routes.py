from flask import redirect, url_for, flash, request, render_template
from flask_login import current_user, login_required
from . import wishlist
from ..extensions import db
from ..models import Wishlist
from ..cards.services import get_card, get_card_smart
from ..activity.services import log_activity


@wishlist.route("/toggle/<card_id>", methods=["POST"])
@login_required
def toggle_wishlist(card_id: str):

    wish_card = Wishlist.query.filter_by(
        user_id=current_user.id,
        card_id=card_id
    ).first()

    if wish_card:
        db.session.delete(wish_card)

        log_activity(
            current_user.id,
            card_id,
            "wishlist_remove"
        )

        message = "Card removed from wishlist."

    else:
        wish_card = Wishlist(
            user_id=current_user.id,
            card_id=card_id
        )

        db.session.add(wish_card)

        log_activity(
            current_user.id,
            card_id,
            "wishlist_add"
        )

        message = "Card added to wishlist."

    db.session.commit()

    flash(message, "success")

    if request.referrer:
        return redirect(request.referrer)

    return redirect(url_for("cards.card_detail", card_id=card_id))


@wishlist.route("/my_wishlist", methods=["GET"])
@login_required
def my_wishlist():

    search = request.args.get("search", "").strip().lower()

    cards_wishlist = []

    for item in current_user.wishlists:

        card_data = get_card_smart(item.card_id)

        if not card_data:
            continue

        if search and search not in card_data.get("name", "").lower():
            continue

        cards_wishlist.append({
            "card": card_data
        })

    return render_template(
        "wishlist/index.html",
        cards_wishlist=cards_wishlist,
        search=search
    )
