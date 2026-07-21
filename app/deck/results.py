from dataclasses import dataclass, asdict
from datetime import datetime
from ..search.results import PaginationResult


@dataclass(slots=True)
class DeckCardSection:

    title: str
    subtitle: str
    cards: list[DeckCardDetail]
    total_cards: int
    unique_cards: int


@dataclass(slots=True)
class DeckCardGroup:

    title: str
    total_cards: int
    unique_cards: int
    sections: list[DeckCardSection]


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
    sections: list[DeckCardSection]
    total_cards: int
    total_unique_cards: int
    created_at: datetime
    updated_at: datetime


@dataclass(slots=True)
class DeckStatistics:

    total_cards: int
    total_unique_cards: int
    pokemon: int
    pokemon_unique: int
    trainers: int
    trainers_unique: int
    energies: int
    energies_unique: int
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
    summary: DeckSummary
    statistics: DeckStatistics


@dataclass(slots=True)
class DeckAjaxSummary:

    total_cards: int
    total_unique_cards: int
    pokemon: int
    trainers: int
    energies: int
    total_value: float
    progress: float


@dataclass(slots=True)
class DeckAjaxSection:

    title: str
    subtitle: str
    total_cards: int
    unique_cards: int


@dataclass(slots=True)
class DeckAjaxResult:

    quantity: int
    removed: bool
    summary: DeckAjaxSummary
    sections: list[DeckAjaxSection]

    def to_dict(self):

        return {
            "quantity": self.quantity,
            "removed": self.removed,
            "summary": asdict(self.summary),
            "sections": [
                asdict(section)
                for section in self.sections
            ]
        }
