from flask import flash, request, redirect, url_for, render_template
from flask_login import login_required, current_user
from . import favorite
from .service import favorite_service
from ..search.filters import SearchFilters
from ..search.service import search_service


@favorite.route("/toggle/<card_id>", methods=["POST"])
@login_required
def toggle_favorite(card_id: str):

    result = favorite_service.toggle(
        user=current_user,
        card_id=card_id
    )

    if result.added:
        message = "Card added to favorites."

    else:
       message = "Card removed from favorites."

    flash(message, "success")

    if request.referrer:
        return redirect(request.referrer)

    return redirect(url_for("cards.card_detail", card_id=card_id))


@favorite.route("/favorite_cards", methods=["GET"])
@login_required
def favorite_cards():
    filters = SearchFilters(request.args)

    context = search_service.get_search_context()

    favorites = favorite_service.get_favorites(current_user, filters)

    return render_template(
        "favorite/index.html",
        favorites=favorites,
        filters=filters,
        **context
    )
