from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True)
class DeckSummary:

    id: int
    name: str
    description: str
    total_crds: int
    total_unique_cards: int
    created_at: datetime
    updated_at: datetime


@dataclass(slots=True)
class DeckCardDetail:

    card_id: str
    name: str
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

    pokemon: int
    trainers: int
    energies: int
    average_hp: int
    total_value: float
