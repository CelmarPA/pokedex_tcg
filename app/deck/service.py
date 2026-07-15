from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import selectinload
from .results import (
    DeckSummary,
    DeckCardDetail,
    DeckDetail,
    DeckStatistics,
    DeckPage,
    AvailableDeckCard,
    DeckAddCardsPage
)
from .validators import DeckValidator
from .card_rules import DeckCardRules
from ..cards.service import card_service
from ..collection.service import collection_service
from ..models import Deck, DeckCard
from ..extensions import db
from .exceptions import (
    DeckNotFoundError,
    DeckCardNotFoundError,
    DeckRuleError
)
from ..search.service import search_service


class DeckService:

    def __init__(self):
        self.validator = DeckValidator()
        self.card_rules = DeckCardRules()

    def create(self, user, name, description):

        name = name.strip()

        self.validator.validate_create(user, name)

        deck = Deck(
            user_id=user.id,
            name=name,
            description=(description or "").strip()
        )

        db.session.add(deck)
        self._commit()

        return self._build_deck_page(deck)

    def update(self, user, deck_id, name, description):

        name = name.strip()

        deck = self._require_deck(user, deck_id)

        self.validator.validate_update(
            user=user,
            deck=deck,
            name=name
        )

        deck.name = name
        deck.description = (description or "").strip()

        self._commit()

        return self._build_deck_page(deck)

    def delete(self, user, deck_id):

        deck = self._require_deck(user, deck_id)

        db.session.delete(deck)
        self._commit()

        return True

    def get_deck(self, user, deck_id):

        deck = self._require_deck(user, deck_id)

        return self._build_deck_page(deck)

    def get_user_decks(self, user, filters):

        decks = []

        for deck in user.decks:

            text = f"{deck.name} {deck.description or ''}"

            if not search_service.match_search(filters.search, text):
                continue

            decks.append(self._build_summary(deck))

        return search_service.paginate(decks, filters)

    def get_card(self, user, deck_id, card_id):

        deck = self._require_deck(user, deck_id)

        deck_card = self._require_deck_card(deck, card_id)

        card_data = card_service.get_card_smart(card_id)

        return self._build_card_detail(deck_card, card_data)

    def add_card(self, user, deck_id, card_id):

        deck = self._require_deck(user, deck_id)

        collection = collection_service.get_card(
            user,
            card_id
        )

        if collection is None:
            raise DeckRuleError(
                "You can only add cards that are in your collection."
            )

        deck_card = self._get_deck_card(deck, card_id)

        card_data = card_service.get_card_smart(
            card_id
        )

        self.card_rules.validate_add_card(
            deck=deck,
            deck_card=deck_card,
            collection=collection,
            card_data=card_data
        )

        if deck_card:

            deck_card.quantity += 1

        else:

            deck.cards.append(
                DeckCard(
                    card_id=card_id,
                    name=card_data.get("name", ""),
                    quantity=1
                )
            )

        self._commit()

        return self._build_deck_page(deck)

    def remove_card(self, user, deck_id, card_id):

        deck = self._require_deck(user, deck_id)

        deck_card = self._require_deck_card(deck, card_id)

        if deck_card.quantity > 1:

            deck_card.quantity -= 1

        else:

            db.session.delete(deck_card)

        self._commit()

        return self._build_deck_page(deck)

    def update_quantity(self, user, deck_id, card_id, quantity):

        deck = self._require_deck(user, deck_id)

        deck_card = self._require_deck_card(deck, card_id)

        collection = collection_service.get_card(
            user,
            card_id
        )

        if collection is None:
            raise DeckRuleError(
                "You can only use cards that are in your collection."
            )

        card_data = card_service.get_card_smart(
            deck_card.card_id
        )

        self.card_rules.validate_quantity(
            deck=deck,
            deck_card=deck_card,
            collection=collection,
            card_data=card_data,
            quantity=quantity
        )

        deck_card.quantity = quantity

        self._commit()

        return self._build_deck_page(deck)

    def get_statistics(self, user, deck_id):

        return self.get_deck(user, deck_id).statistics

    def get_available_cards(self, user, deck_id, filters):

        deck = self._require_deck(user, deck_id)

        collection = collection_service.get_user_cards_with_data(user)

        deck_cards = {
            card.card_id: card
            for card in deck.cards
        }

        available = []

        for item in collection:

            if not search_service.match_filters(filters, item.card):
                continue

            deck_card = deck_cards.get(
                item.card["id"]
            )

            deck_quantity = (
                deck_card.quantity
                if deck_card
                else 0
            )

            if self.card_rules.is_basic_energy(item.card):

                max_quantity = item.quantity

            else:

                max_quantity = min(
                    4,
                    item.quantity
                )

            if deck_quantity >= max_quantity:
                continue

            available.append(

                AvailableDeckCard(
                    card=item.card,
                    collection_quantity=item.quantity,
                    deck_quantity=deck_quantity,
                    max_quantity=max_quantity
                )

            )

        return search_service.paginate(available, filters)

    def get_add_cards_page(self, user, deck_id, filters):

        page = self.get_deck(user, deck_id)

        cards = self.get_available_cards(user, deck_id, filters)

        return DeckAddCardsPage(
            deck=page.deck,
            statistics=page.statistics,
            cards=cards
        )

    def _get_deck(self, user, deck_id):
        return (
            Deck.query
            .options(
                selectinload(Deck.cards)
            )
            .filter_by(
                id=deck_id,
                user_id=user.id
            )
            .first()
        )

    def _get_deck_card(self, deck, card_id):

        return next(
            (
                card
                for card in deck.cards
                if card.card_id == card_id
            ),
            None
        )

    def _require_deck(self, user, deck_id):

        deck = self._get_deck(user, deck_id)

        if deck is None:
            raise DeckNotFoundError()

        return deck

    def _require_deck_card(self, deck, card_id):
        deck_card = self._get_deck_card(deck, card_id)

        if deck_card is None:
            raise DeckCardNotFoundError()

        return deck_card

    def _count_cards(self, deck):
        return sum(
            card.quantity
            for card in deck.cards
        )

    def _count_unique_cards(self, deck):
        return len(deck.cards)

    def _build_summary(self, deck):
        return DeckSummary(
            id=deck.id,
            name=deck.name,
            description=deck.description,
            total_cards=self._count_cards(deck),
            total_unique_cards=self._count_unique_cards(deck),
            created_at=deck.created_at,
            updated_at=deck.updated_at
        )

    def _build_card_detail(self, deck_card, card_data):
        return DeckCardDetail(
            card_id=deck_card.card_id,
            quantity=deck_card.quantity,
            card_data=card_data
        )

    def _build_deck_detail(self, deck, cards_data):
        cards = [
            DeckCardDetail(
                card_id=card.card_id,
                quantity=card.quantity,
                card_data=cards_data.get(
                    card.card_id
                )
            )
            for card in sorted(
                deck.cards,
                key=lambda card: card.name
            )
        ]

        return DeckDetail(
            id=deck.id,
            name=deck.name,
            description=deck.description,
            cards=cards,
            total_cards=self._count_cards(deck),
            total_unique_cards=self._count_unique_cards(deck),
            created_at=deck.created_at,
            updated_at=deck.updated_at
        )

    def _build_statistics(
            self,
            deck,
            cards_data
    ):
        total_cards = self._count_cards(deck)
        total_unique_cards = self._count_unique_cards(deck)

        pokemon = 0
        trainers = 0
        energies = 0

        hp_total = 0
        hp_count = 0

        total_value = 0

        for deck_card in deck.cards:

            card_data = cards_data.get(
                deck_card.card_id
            )

            if card_data is None:
                continue

            # Calculate statistics
            quantity = deck_card.quantity

            supertype = card_data.get("supertype")

            # Pokémon
            if supertype == "Pokémon":

                pokemon += quantity

                hp = card_data.get("hp")

                if hp:

                    try:

                        hp_total += int(hp) * quantity
                        hp_count += quantity

                    except ValueError:
                        pass

            # Trainer
            elif supertype == "Trainer":

                trainers += quantity

            # Energy
            elif supertype == "Energy":

                energies += quantity

            # Market Value
            total_value += (
                    card_service
                    .get_market_prices(card_data)
                    .market
                    * quantity
            )

        average_hp = (
            hp_total // hp_count
            if hp_count else 0
        )

        average_price = (
            round(total_value / total_cards, 2)
            if total_cards
            else 0
        )

        pokemon_percentage = (pokemon / total_cards * 100) if total_cards else 0
        trainers_percentage = (trainers / total_cards * 100) if total_cards else 0
        energies_percentage = (energies / total_cards * 100) if total_cards else 0

        return DeckStatistics(
            total_cards=total_cards,
            total_unique_cards=total_unique_cards,
            pokemon=pokemon,
            trainers=trainers,
            energies=energies,
            average_hp=average_hp,
            average_price=average_price,
            total_value=round(total_value, 2),
            pokemon_percentage=pokemon_percentage,
            trainers_percentage=trainers_percentage,
            energies_percentage=energies_percentage
        )

    def _build_deck_page(self, deck):
        card_ids = [
            card.card_id
            for card in deck.cards
        ]

        cards_data = card_service.get_cards_smart(card_ids)

        detail = self._build_deck_detail(deck, cards_data)

        statistics = self._build_statistics(deck, cards_data)

        return DeckPage(
            deck=detail,
            statistics=statistics
        )

    def _commit(self):
        try:
            db.session.commit()

        except SQLAlchemyError:
            db.session.rollback()
            raise


deck_service = DeckService()
