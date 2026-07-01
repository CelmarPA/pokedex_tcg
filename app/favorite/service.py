from ..models import Favorite
from ..extensions import db
from ..activity.services import log_activity
from ..cards.service import card_service
from .results import ToggleResult
from ..search.service import match_search


class FavoriteService:

    def toggle(self, user, card_id):

        favorite = Favorite.query.filter_by(
            user_id=user.id,
            card_id=card_id
        ).first()

        if favorite:

            db.session.delete(favorite)
            added = False
            action = "favorite_remove"

        else:

            favorite = Favorite(
                user_id=user.id,
                card_id=card_id
            )

            db.session.add(favorite)

            added = True
            action = "favorite_add"

        log_activity(
            user_id=user.id,
            card_id=card_id,
            action=action
        )

        db.session.commit()

        return ToggleResult(
            added=added
        )

    def get_favorites(self, user, filters):

        search = filters.search.casefold()

        favorites = []

        for item in user.favorites:

            card_data = card_service.get_card_smart(item.card_id)

            if not card_data:
                continue

            if not match_search(search, card_data.get("name", "")):
                continue

            favorites.append({
                "card": card_data
            })

        return favorites


favorite_service = FavoriteService()
