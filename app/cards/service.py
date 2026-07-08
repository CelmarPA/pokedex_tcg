import requests
import os
from datetime import datetime, UTC
from app.models import CardCache
from .results import CardDetail, MarketPrices
from ..extensions import db
from ..search.pagination import Pagination
from ..search.results import CardSearchResult
from ..search.service import search_service
from ..models import Collection, Favorite, Wishlist


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

        query = search_service.build_query(filters)

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

        cache = CardCache.query.get(
            card_data["id"]
        )

        if cache:

            cache.data = card_data

        else:

            cache = CardCache(
                id=card_data["id"],
                name=card_data.get("name"),
                data=card_data
            )

            db.session.add(cache)

        return cache

    def get_card_smart(self, card_id: str):

        cached = db.session.get(
            CardCache,
            card_id
        )

        if cached:
            return cached.data

        card = self.get_card(card_id)

        if not card:
            return None

        self.cache_card(card)

        db.session.commit()

        return card

    def get_cards_smart(self, card_ids: list[str]) -> dict:

        if not card_ids:
            return {}

        cards = {}

        # 1. Retrieve all existing cards from the cache at once
        cached_cards = (
            CardCache.query
            .filter(
                CardCache.id.in_(card_ids)
            )
            .all()
        )

        for cached in cached_cards:
            cards[cached.id] = cached.data

        # 2. Find out which ones were missing from the cache
        missing_ids = [
            card_id
            for card_id in card_ids
            if card_id not in cards
        ]

        # 3. Search for missing items in the API
        for card_id in missing_ids:

            card = self.get_card(card_id)

            if card:
                self.cache_card(card)

                cards[card_id] = card

        db.session.commit()

        return cards

    def get_market_prices(self, card_data: dict) -> MarketPrices:

        market = []
        low = []
        mid = []
        high = []

        prices = card_data.get("tcgplayer", {}).get("prices", {})

        if not prices:
            return MarketPrices(
                market=0,
                low=0,
                mid=0,
                high=0
            )

        for price_data in prices.values():
            if price_data.get("market") is not None:
                market.append(price_data["market"])

            if price_data.get("low") is not None:
                low.append(price_data["low"])

            if price_data.get("mid") is not None:
                mid.append(price_data["mid"])

            if price_data.get("high") is not None:
                high.append(price_data["high"])

        return MarketPrices(
            market=max(market) if market else 0,
            low=min(low) if low else 0,
            mid=max(mid) if mid else 0,
            high=max(high) if high else 0
        )

    def get_card_detail(self, user, card_id):

        card_data = self.get_card_smart(card_id)

        prices = self.get_market_prices(card_data)

        if user.is_authenticated:
            collection_card = Collection.query.filter_by(
                user_id=user.id,
                card_id=card_id
            ).first()

            favorite_card = Favorite.query.filter_by(
                user_id=user.id,
                card_id=card_id
            ).first()

            cards_wishlist = Wishlist.query.filter_by(
                user_id=user.id,
                card_id=card_id
            ).first()

        else:
            collection_card = None
            favorite_card = None
            cards_wishlist = None

        return CardDetail(
            card_data=card_data,
            prices=prices,
            collection_card=collection_card,
            favorite_card=favorite_card,
            cards_wishlist=cards_wishlist,
        )


card_service = CardService()
