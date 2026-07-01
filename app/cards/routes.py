from flask import render_template, request
from flask_login import current_user
from . import cards
from ..models import Collection, Favorite, Wishlist
from ..search.filters import SearchFilters
from ..search.service import get_search_context
from .service import card_service


@cards.route("/")
def index():
    filters = SearchFilters(request.args)

    result = card_service.get_cards(filters)

    context = get_search_context()

    return render_template(
        "cards/index.html",
        cards=result.cards,
        pagination=result.pagination,
        filters=filters,
        **context
    )


@cards.route("/<card_id>", methods=["GET"])
def card_detail(card_id: str):

    card_data = card_service.get_card_smart(card_id)

    prices = card_service.get_market_prices(card_data)

    if current_user.is_authenticated:
        collection_card = Collection.query.filter_by(
            user_id=current_user.id,
            card_id=card_id
        ).first()

        favorite_card = Favorite.query.filter_by(
            user_id=current_user.id,
            card_id=card_id
        ).first()

        cards_wishlist = Wishlist.query.filter_by(
            user_id=current_user.id,
            card_id=card_id
        ).first()

    else:
        collection_card = None
        favorite_card = None
        cards_wishlist = None

    print(card_data)

    return render_template(
        "cards/detail.html",
        card=card_data,
        prices=prices,
        collection_card=collection_card,
        favorite_card=favorite_card,
        cards_wishlist=cards_wishlist
    )
