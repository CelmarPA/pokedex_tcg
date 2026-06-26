import os
import requests
from datetime import datetime, UTC
from app.models import CardCache
from ..extensions import db


API_URL = "https://api.pokemontcg.io/v2/cards"

HEADERS = {
    "X-Api-Key": os.getenv("POKEMON_TCG_API_KEY")
}


def get_cards(search=None, page_size=20):
    search = search.strip()

    params = {
        "pageSize": page_size
    }

    if " " in search:
        params["q"] = f'name:"{search}"'
    else:
        params["q"] = f"name:*{search}*"

    response = requests.get(
        API_URL,
        headers=HEADERS,
        params=params
    )

    response.raise_for_status()

    return response.json()["data"]


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
    cache = CardCache(
        id=card_id,
        name=card.get("name"),
        data=card,
        updated_at=datetime.now(UTC)
    )

    db.session.add(cache)
    db.session.commit()

    return card