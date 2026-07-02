from ..cards.service import card_service
from .results import CollectionProgress, CollectionCard
from ..search.service import search_service


class CollectionService:

    def get_collection_value(self, user):

        collection_value = 0

        for item in user.collections:
            card_data = card_service.get_card_smart(item.card_id)

            market_price = card_service.get_market_prices(card_data)

            collection_value += (market_price.market * item.quantity)

        return collection_value

    def get_collection_progress(self, user):

        progress = {}

        for item in user.collections:
            card = card_service.get_card_smart(item.card_id)

            card_set = card["set"]
            set_id = card_set["id"]

            set_images = card["set"]["images"]

            if set_id not in progress:
                progress[set_id] = CollectionProgress(
                    set_id=set_id,
                    set_name=card_set["name"],
                    series=card_set["series"],
                    owned=0,
                    total=card_set["printedTotal"],
                    symbol=set_images["symbol"],
                    logo=set_images["logo"],
                )

            progress[set_id].owned += 1

        for set_data in progress.values():
            set_data.progress = round(
                (set_data.owned / set_data.total) * 100,
                1
            )

        return sorted(
            progress.values(),
            key=lambda x: x.progress,
            reverse=True
        )

    def get_collection(self, user,filters):

        search = filters.search

        cards_collection = []

        for item in user.collections:

            card_data = card_service.get_card_smart(item.card_id)

            if not card_data:
                continue

            if not search_service.match_search(search, card_data.get("name", "")):
                continue

            cards_collection.append(CollectionCard(
                card=card_data,
                quantity=item.quantity
            ))

        return cards_collection


collection_service = CollectionService()
