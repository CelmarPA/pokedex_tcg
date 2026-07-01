from ..models import Wishlist
from ..extensions import db
from ..activity.services import log_activity
from .results import ToggleResult
from ..cards.service import card_service
from ..search.service import match_search


class WishlistService:

    def toggle(self, user, card_id):

        wish_card = Wishlist.query.filter_by(
            user_id=user.id,
            card_id=card_id
        ).first()

        if wish_card:

            db.session.delete(wish_card)
            added = False
            action = "wishlist_remove"

        else:
            wish_card = Wishlist(
                user_id=user.id,
                card_id=card_id
            )

            db.session.add(wish_card)

            added = True
            action = "wishlist_add"

        log_activity(
            user_id=user.id,
            card_id=card_id,
            action=action
        )

        db.session.commit()

        return ToggleResult(
            added=added
        )

    def get_my_wishlist(self, user, filters):

        search = filters.search.casefold()

        cards_wishlist = []

        for item in user.wishlists:

            card_data = card_service.get_card_smart(item.card_id)

            if not card_data:
                continue

            if not match_search(search, card_data.get("name", "")):
                continue

            cards_wishlist.append({
                "card": card_data
            })

        return cards_wishlist

wishlist_service = WishlistService()
