from dataclasses import dataclass
from datetime import datetime
from ..search.results import PaginationResult


@dataclass(slots=True)
class DeckSummary:

    id: int
    name: str
    description: str
    total_cards: int
    total_unique_cards: int
    created_at: datetime
    updated_at: datetime


@dataclass(slots=True)
class DeckCardDetail:

    card_id: str
    quantity: int
    card_data: dict


@dataclass(slots=True)
class DeckDetail:

    id: int
    name: str
    description: str
    cards: list[DeckCardDetail]
    total_cards: int
    total_unique_cards: int
    created_at: datetime
    updated_at: datetime


@dataclass(slots=True)
class DeckStatistics:

    total_cards: int
    total_unique_cards: int
    pokemon: int
    trainers: int
    energies: int
    average_hp: int
    average_price: float
    total_value: float
    pokemon_percentage: float
    trainers_percentage: float
    energies_percentage: float


@dataclass(slots=True)
class AvailableDeckCard:

    card: dict
    collection_quantity: int
    deck_quantity: int
    max_quantity: int


@dataclass(slots=True)
class DeckAddCardsPage:

    deck: object
    statistics: object
    cards: PaginationResult


@dataclass(slots=True)
class DeckPage:

    deck: DeckDetail
    statistics: DeckStatistics