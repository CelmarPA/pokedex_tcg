from flask import render_template, request
from . import cards
from .services import get_cards, get_card


@cards.route("/")
def index():
    search = request.args.get("search", "").strip()

    cards_data = get_cards(search=search)

    return render_template("cards/index.html", cards=cards_data, search=search)


@cards.route("/<card_id>", methods=["GET"])
def card_detail(card_id: str):
    print(card_id)
    card_data = get_card(card_id)

    return render_template("cards/detail.html", card=card_data)