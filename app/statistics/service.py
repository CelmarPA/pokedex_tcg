from ..collection.service import collection_service
from ..cards.service import card_service
from .results import Statistics, ChartData, CollectionRarity, CollectionType, MostOwnedCard
from collections import Counter

from ..favorite.service import favorite_service
from ..wishlist.service import wishlist_service


class StatisticsService:

    def _get_collection_cards(self, user):

        cards = []

        for item in user.collections:

            card_data = card_service.get_card_smart(item.card_id)

            if card_data:
                cards.append((item, card_data))

        return cards

    def _count_by_attribute(self, user, attribute, default="Unknown"):

        counter = Counter()

        for item, card in self._get_collection_cards(user):

            value = card.get(attribute, default)

            counter[value] += item.quantity

        return counter

    def _count_types(self, user):

        counter = Counter()

        for item, card in self._get_collection_cards(user):

            for pokemon_type in card.get("types", []):
                counter[pokemon_type] += item.quantity

        return counter

    def get_user_statistics(self, user):

        total_cards = collection_service.get_total_cards(user)

        unique_cards = collection_service.get_unique_cards(user)

        favorite_count = favorite_service.get_favorite_count(user)

        wishlist_count = wishlist_service.get_wishlist_count(user)

        collection_value = collection_service.get_collection_value(user)

        collection = max(
            user.collections,
            key=lambda card: card.quantity
        )

        most_owned = MostOwnedCard(
            collection=collection,
            card_data=card_service.get_card_smart(collection.card_id)
        )

        return Statistics(
            total_cards=total_cards,
            unique_cards=unique_cards,
            favorite_count=favorite_count,
            wishlist_count=wishlist_count,
            most_owned=most_owned,
            collection_value=collection_value
        )

    def get_collection_progress(self, user):

        return collection_service.get_collection_progress(user)

    def get_favorite_types(self, user):

        types = self._count_types(user)

        return [
            CollectionType(
                type=pokemon_type,
                count=count
            )
            for pokemon_type, count in types.most_common()
        ]

    def get_collection_rarity(self, user):

        rarities = self._count_by_attribute(
            user,
            attribute="rarity"
        )

        return [
            CollectionRarity(
                rarity=rarity,
                count=count
            )
            for rarity, count in rarities.most_common()
        ]

    def get_types_chart(self, user):

        favorite_types = self.get_favorite_types(user)

        return ChartData(
            labels=[item.type for item in favorite_types],
            values=[item.count for item in favorite_types]
        )

    def get_rarity_chart(self, user):

        collection_rarity = self.get_collection_rarity(user)

        return ChartData(
            labels=[item.rarity for item in collection_rarity],
            values=[item.count for item in collection_rarity]
        )


statistics_service = StatisticsService()