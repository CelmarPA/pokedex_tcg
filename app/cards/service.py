import requests
import os
from datetime import datetime, UTC
from app.models import CardCache
from ..extensions import db
from ..search.pagination import Pagination
from ..search.results import CardSearchResult
from ..search.service import build_query
# from ..search.service import search_service

class CardService:


    def __init__(self):
        self.api_url = "https://api.pokemontcg.io/v2/cards"

        self.headers = {
        "X-Api-Key": os.getenv("POKEMON_TCG_API_KEY")
        }

    def get_cards(self, filters=None):

        params = {
            "page": filters.page,
            "pageSize": filters.page_size
        }

        if filters:

            query = build_query(filters)

            # query = search_service.build_query(filters)

            if query:
                params["q"] = query

        response = requests.get(
            self.api_url,
            headers=self.headers,
            params=params
        )

        response.raise_for_status()

        data = response.json()

        cards = data["data"]

        pagination = Pagination(
            page=data["page"],
            page_size=data["pageSize"],
            count=data["count"],
            total_count=data["totalCount"]
        )

        for card in cards:
            card["prices"] = self.get_market_prices(card)

        return CardSearchResult(
            cards=cards,
            pagination=pagination
        )

    def get_card(self, card_id:str):

        response = requests.get(
            url=f"{self.api_url}/{card_id}",
            headers=self.headers
        )

        response.raise_for_status()

        return response.json()["data"]

    def cache_card(self, card_data):
        cache = CardCache(
            id=card_data["id"],
            name=card_data.get("name"),
            data=card_data,
            updated_at=datetime.now(UTC)
        )

        db.session.add(cache)
        db.session.commit()

    def get_card_smart(self, card_id: str):

        cached = CardCache.query.get(card_id)

        # 1. try cache in the database
        if cached:
            return cached.data

        # 2. fallback API
        card = self.get_card(card_id)

        if not card:
            return None

        # save in cache
        self.cache_card(card)

        return card

    def get_market_prices(self, card_data):

        market = []
        low = []
        mid = []
        high = []

        prices = card_data.get("tcgplayer", {}).get("prices", {})

        if not prices:
            return {
                "market": 0,
                "low": 0,
                "mid": 0,
                "high": 0
            }

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


card_service = CardService()