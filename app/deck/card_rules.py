from ..models import Deck
from .exceptions import DeckRuleError


class DeckCardRules:


    @staticmethod
    def is_basic_energy(card_data):

        return (
            card_data.get("supertype") == "Energy"
            and "Basic" in card_data.get("subtypes", [])
        )

    def validate_add_card(
        self,
        deck,
        deck_card,
        collection,
        card_data
    ):

        self.validate_max_cards(deck)

        self.validate_collection_quantity(
            deck_card,
            collection
        )

        self.validate_duplicate(
            deck_card,
            card_data
        )

    def validate_quantity(
        self,
        deck,
        deck_card,
        collection,
        card_data,
        quantity
    ):

        self.validate_min_quantity(quantity)

        self.validate_collection_quantity_update(
            collection,
            quantity
        )

        self.validate_duplicate_quantity(
            card_data,
            quantity
        )

        self.validate_max_cards_quantity(
            deck,
            deck_card,
            quantity
        )

    def validate_max_cards(self, deck):

        total = sum(
            card.quantity
            for card in deck.cards
        )

        if total >= 60:
            raise DeckRuleError(
                "A deck cannot contain more than 60 cards."
            )

    def validate_duplicate(
        self,
        deck_card,
        card_data
    ):

        if deck_card is None:
            return

        if self.is_basic_energy(card_data):
            return

        if deck_card.quantity >= 4:
            raise DeckRuleError(
                "A deck cannot contain more than 4 copies of the same card."
            )

    def validate_min_quantity(self, quantity):

        if quantity < 1:
            raise DeckRuleError(
                "Quantity must be at least 1."
            )

    def validate_duplicate_quantity(
        self,
        card_data,
        quantity
    ):

        if self.is_basic_energy(card_data):
            return

        if quantity > 4:
            raise DeckRuleError(
                "A deck cannot contain more than 4 copies of the same card."
            )

    def validate_max_cards_quantity(
        self,
        deck,
        deck_card,
        quantity
    ):

        total = (
            sum(
                card.quantity
                for card in deck.cards
            )
            - deck_card.quantity
            + quantity
        )

        if total > 60:
            raise DeckRuleError(
                "A deck cannot contain more than 60 cards."
            )

    def validate_collection_quantity(
            self,
            deck_card,
            collection
    ):

        new_quantity = (
            deck_card.quantity + 1
            if deck_card
            else 1
        )

        if new_quantity > collection.quantity:
            raise DeckRuleError(
                "You don't have enough copies of this card in your collection."
            )

    def validate_collection_quantity_update(
            self,
            collection,
            quantity
    ):

        if quantity > collection.quantity:
            raise DeckRuleError(
                "You don't have enough copies of this card in your collection."
            )