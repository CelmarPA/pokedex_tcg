from .validators import DeckValidator
from ..models import Deck
from ..extensions import db


class DeckService:

    def __init__(self):
        self.validator = DeckValidator()

    def create(self, user, name, description):

        self.validator.validate_create(user, name)

        deck = Deck(
            user_id=user.id,
            name=name.strip(),
            description=(description or "").strip()
        )

        db.session.add(deck)
        db.session.commit()

        return deck

    def update(self):
        pass

    def delete(self):
        pass

    def get_deck(self, deck_id):
        pass

    def get_user_decks(self, user):
        pass

    def get_card(self, deck, card_id):
        pass

    def add_card(self, deck, card_id):
        pass

    def remove_card(self, deck, card_id):
        pass

    def change_quantity(self, deck, card_id, quantity):
        pass

    def get_statistics(self):
        pass
