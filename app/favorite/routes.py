from flask import flash, request, redirect, url_for, render_template
from flask_login import login_required, current_user
from . import favorite
from ..models import Favorite
from ..extensions import db
from ..cards.services import get_card_smart
from ..activity.services import log_activity
from ..search.filters import SearchFilters
from ..search.services import get_search_context


@favorite.route("/toggle/<card_id>", methods=["POST"])
@login_required
def toggle_favorite(card_id: str):

    favorite_card = Favorite.query.filter_by(
        user_id=current_user.id,
        card_id=card_id
    ).first()

    if favorite_card:

        db.session.delete(favorite_card)

        log_activity(
            current_user.id,
            card_id,
            "favorite_remove"
        )

        message = "Card removed from favorites."

    else:

        favorite_card = Favorite(
            user_id=current_user.id,
            card_id=card_id
        )

        db.session.add(favorite_card)

        log_activity(
            current_user.id,
            card_id,
            "favorite_add"
        )

        message = "Card added to favorites."

    db.session.commit()

    flash(message, "success")

    if request.referrer:
        return redirect(request.referrer)

    return redirect(url_for("cards.card_detail", card_id=card_id))


@favorite.route("/favorite_cards", methods=["GET"])
@login_required
def favorite_cards():
    filters = SearchFilters(request.args)

    search = (filters.search or "").lower().strip()

    context = get_search_context()

    favorites = []

    for item in current_user.favorites:

        card_data = get_card_smart(item.card_id)

        if not card_data:
            continue

        if search and search not in card_data.get("name", "").lower():
            continue

        favorites.append({
            "card": card_data
        })

    return render_template(
        "favorite/index.html",
        favorites=favorites,
        filters=filters,
        **context
    )
