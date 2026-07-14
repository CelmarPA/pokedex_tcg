from flask import redirect, url_for, flash, request, render_template
from flask_login import current_user, login_required
from . import wishlist
from ..search.filters import SearchFilters
from ..search.service import search_service
from .service import wishlist_service


@wishlist.route("/toggle/<card_id>", methods=["POST"])
@login_required
def toggle_wishlist(card_id: str):

    result = wishlist_service.toggle(
        user=current_user,
        card_id=card_id
    )

    if result.added:
        message = "Card added to wishlist."

    else:
        message = "Card removed from wishlist."


    flash(message, "success")

    if request.referrer:
        return redirect(request.referrer)

    return redirect(url_for("cards.card_detail", card_id=card_id))


@wishlist.route("/my_wishlist", methods=["GET"])
@login_required
def my_wishlist():

    filters = SearchFilters(request.args)

    context = search_service.get_search_context()

    cards_wishlist = wishlist_service.get_wishlist(current_user, filters)

    return render_template(
        "wishlist/index.html",
        cards_wishlist=cards_wishlist,
        pagination=cards_wishlist.pagination,
        filters=filters,
        **context
    )
