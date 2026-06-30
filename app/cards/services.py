import os
import requests
from datetime import datetime, UTC
from app.models import CardCache
from ..extensions import db
from ..search.services import build_query


API_URL = "https://api.pokemontcg.io/v2/cards"

HEADERS = {
    "X-Api-Key": os.getenv("POKEMON_TCG_API_KEY")
}


def get_cards(filters=None, page_size=20):

    params = {
        "pageSize": page_size
    }

    if filters:

        query = build_query(filters)

        if query:
            params["q"] = query

    response = requests.get(
        API_URL,
        headers=HEADERS,
        params=params
    )

    response.raise_for_status()

    cards = response.json()["data"]

    for card in cards:
        card["prices"] = get_card_prices(card)

    return cards


def get_card(card_id: str):

    response = requests.get(
        url=API_URL + f"/{card_id}",
        headers=HEADERS
    )

    response.raise_for_status()

    return response.json()["data"]


def get_card_smart(card_id: str):

    cached = CardCache.query.get(card_id)

    # 1. try cache in the database
    if cached:
        return cached.data

    # 2. fallback API
    card = get_card(card_id)

    if not card:
        return None

    # save in cache
    cache_card(card)

    return card


def cache_card(card_data):

    cache = CardCache(
        id=card_data["id"],
        name=card_data.get("name"),
        data=card_data,
        updated_at=datetime.now(UTC)
    )

    db.session.add(cache)
    db.session.commit()


def get_card_prices(card_data):

    prices = card_data.get("tcgplayer", {}).get("prices", {})

    if not prices:
        return {
            "market": 0,
            "low": 0,
            "mid": 0,
            "high": 0
        }

    market = []
    low = []
    mid = []
    high = []

    for price_data in prices.values():
        if price_data.get("market") is not None:
            market.append(price_data["market"])

        if price_data.get("low") is not None:
            low.append(price_data["low"])

        if price_data.get("mid") is not None:
            mid.append(price_data["mid"])

        if price_data.get("high") is not None:
            high.append(price_data["high"])

    return {
        "market": max(market) if market else 0,
        "low": min(low) if low else 0,
        "mid": max(mid) if mid else 0,
        "high": max(high) if high else 0
    }
