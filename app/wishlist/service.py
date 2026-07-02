from ..models import Wishlist
from ..extensions import db
from ..activity.service import activity_service
from .results import ToggleResult, WishlistCard
from ..cards.service import card_service
from ..search.service import search_service


class WishlistService:

    def toggle(self, user, card_id):

        wishlist_card = Wishlist.query.filter_by(
            user_id=user.id,
            card_id=card_id
        ).first()

        if wishlist_card:

            db.session.delete(wishlist_card)
            added = False
            action = "wishlist_remove"

        else:
            wishlist_card = Wishlist(
                user_id=user.id,
                card_id=card_id
            )

            db.session.add(wishlist_card)

            added = True
            action = "wishlist_add"

        activity_service.log_activity(
            user_id=user.id,
            card_id=card_id,
            action=action
        )

        db.session.commit()

        return ToggleResult(
            added=added
        )

    def get_wishlist(self, user, filters):

        search = filters.search

        cards_wishlist = []

        for item in user.wishlists:

            card_data = card_service.get_card_smart(item.card_id)

            if not card_data:
                continue

            if not search_service.match_search(search, card_data.get("name", "")):
                continue

            cards_wishlist.append(WishlistCard(
                card=card_data
            ))

        return cards_wishlist

wishlist_service = WishlistService()
