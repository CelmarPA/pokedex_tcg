from sqlalchemy import func
from .exceptions import (
    DeckValidationError,
    DeckRuleError
)
from ..models import Deck


class DeckValidator:

    def validate_create(
        self,
        user,
        name
    ):

        if self._find_by_name(user, name):
            raise DeckValidationError(
                "You already have a deck with this name."
            )

    def validate_update(self, user, deck, name):

        exists = self._find_by_name(user, name)

        if exists and exists.id != deck.id:
            raise DeckValidationError(
                "You already have a deck with this name."
            )

    def _find_by_name(self, user, name):
        return Deck.query.filter(
            Deck.user_id == user.id,
            func.lower(Deck.name) == name.lower()
        ).first()
