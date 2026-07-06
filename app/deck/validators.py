from ..models import Deck


class DeckValidator:

    def validate_create(self, user, name):

        exists = Deck.query.filter_by(
            user_id=user.id,
            name=name
        ).first()

        if exists:
            raise ValueError(
                "You already have a deck with this name."
            )


    def validate_quantity(self, deck, card_id, quantity):
        pass

    def validate_max_cards(self, deck):
        pass

    def validate_duplicate(self, deck, card_id):
        pass