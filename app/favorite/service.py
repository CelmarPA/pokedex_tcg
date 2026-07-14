from ..models import Favorite
from ..extensions import db
from ..activity.service import activity_service
from ..cards.service import card_service
from .results import ToggleResult, FavoriteCard
from ..search.service import search_service


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

        activity_service.log_activity(
            user_id=user.id,
            card_id=card_id,
            action=action
        )

        db.session.commit()

        return ToggleResult(
            added=added
        )

    def get_favorites(self, user, filters):

        favorites = []

        for item in user.favorites:

            card_data = card_service.get_card_smart(item.card_id)

            if not card_data:
                continue

            if not search_service.match_filters(filters, card_data):
                continue

            favorites.append(FavoriteCard(
                card=card_data
            ))

        return search_service.paginate(favorites, filters)

    def get_favorite_count(self, user):

        return len(user.favorites)


favorite_service = FavoriteService()
