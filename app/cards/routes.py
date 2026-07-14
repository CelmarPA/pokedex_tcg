from flask import render_template, request
from flask_login import current_user
from . import cards
from ..search.filters import SearchFilters
from ..search.service import search_service
from .service import card_service


@cards.route("/")
def index():
    filters = SearchFilters(request.args)

    result = card_service.get_cards(filters)

    context = search_service.get_search_context()

    return render_template(
        "cards/index.html",
        cards=result.items,
        pagination=result.pagination,
        filters=filters,
        **context
    )


@cards.route("/<card_id>", methods=["GET"])
def card_detail(card_id: str):

    details = card_service.get_card_detail(current_user, card_id)

    return render_template(
        "cards/detail.html",
        details=details
    )
