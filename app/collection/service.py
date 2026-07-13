from ..cards.service import card_service
from .results import CollectionProgress, CollectionCard
from ..search.service import search_service
from ..models import Collection
from ..extensions import db
from ..activity.service import activity_service


class CollectionService:

    def add_card_to_collection(self, user, card_id):

        card = Collection.query.filter_by(
            user_id=user.id,
            card_id=card_id
        ).first()

        if not card:
            card = Collection(
                user_id=user.id,
                card_id=card_id,
                quantity=1
            )

            db.session.add(card)

        else:
            card.quantity += 1

        activity_service.log_activity(
            user.id,
            card_id,
            "collection_add"
        )

        db.session.commit()

    def remove_card_from_collection(self, user, card_id):

        card = Collection.query.filter_by(
            user_id=user.id,
            card_id=card_id
        ).first()

        if not card:
            return None

        removed_last_copy = (card.quantity == 1)

        if removed_last_copy:
            db.session.delete(card)

        else:
            card.quantity -= 1


        activity_service.log_activity(
            user.id,
            card_id,
            "collection_remove"
        )

        db.session.commit()

        return removed_last_copy

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

    def get_total_cards(self, user):

        return sum(item.quantity for item in user.collections)

    def get_unique_cards(self, user):

        return len(user.collections)

    def _get_collection_card(self, user, card_id):

        return Collection.query.filter_by(
            user_id=user.id,
            card_id=card_id
        ).first()

    def get_card(self, user, card_id):

        collection = self._get_collection_card(
            user,
            card_id
        )

        if collection is None:
            return None

        return collection

    def get_user_cards_with_data(self, user):

        card_ids = [
            item.card_id
            for item in user.collections
        ]

        cards_data = card_service.get_cards_smart(
            card_ids
        )

        return [
            self._build_collection_card(
                item,
                cards_data[item.card_id]
            )
            for item in user.collections
            if item.card_id in cards_data
        ]

    def _build_collection_card(self, collection, card_data):

        return CollectionCard(
            card=card_data,
            quantity=collection.quantity
        )


collection_service = CollectionService()
