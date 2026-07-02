from ..collection.service import collection_service
from ..cards.service import card_service
from .results import Statistics
from collections import Counter


class StatisticsService:

    def get_user_statistics(self, user):

        total_cards = sum(card.quantity for card in user.collections)

        unique_cards = len(user.collections)

        favorite_count = len(user.favorites)

        wishlist_count = len(user.wishlists)

        most_owned_card = None
        most_owned_card_data = None

        collection_value = collection_service.get_collection_value(user)

        if user.collections:

            most_owned_card = max(
                user.collections,
                key=lambda card: card.quantity
            )

            if most_owned_card:
                most_owned_card_data = card_service.get_card_smart(most_owned_card.card_id)

        return Statistics(
            total_cards=total_cards,
            unique_cards=unique_cards,
            favorite_count=favorite_count,
            wishlist_count=wishlist_count,
            most_owned_card=most_owned_card,
            most_owned_card_data=most_owned_card_data,
            collection_value=collection_value
        )

    def get_collection_progress(self, user):

        return collection_service.get_collection_progress(user)

    def get_favorite_types(self, user):

        types = Counter()

        for item in user.collections:

            card = card_service.get_card_smart(item.card_id)

            for pokemon_type in card.get("types", []):
                types[pokemon_type] += item.quantity

        return [
            {
                "type": pokemon_type,
                "count": count
            }
            for pokemon_type, count in types.most_common()
        ]

    def get_collection_rarity(self, user):

        rarities = Counter()

        for item in user.collections:
            card = card_service.get_card_smart(item.card_id)

            rarity = card.get("rarity", "Unknown")

            rarities[rarity] += item.quantity

        return [
            {
                "rarity": rarity,
                "count": count
            }
            for rarity, count in rarities.most_common()
        ]


statistics_service = StatisticsService()