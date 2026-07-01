from flask import redirect, url_for, flash, request, render_template
from flask_login import current_user, login_required
from . import wishlist
from ..extensions import db
from ..models import Wishlist
from ..cards.service import card_service
from ..activity.services import log_activity
from ..search.filters import SearchFilters
from ..search.service import get_search_context, match_search


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

    filters = SearchFilters(request.args)

    search = filters.search.casefold()

    context = get_search_context()

    cards_wishlist = []

    for item in current_user.wishlists:

        card_data = card_service.get_card_smart(item.card_id)

        if not card_data:
            continue

        if not match_search(search, card_data.get("name", "")):
            continue

        cards_wishlist.append({
            "card": card_data
        })

    return render_template(
        "wishlist/index.html",
        cards_wishlist=cards_wishlist,
        filters=filters,
        **context
    )
