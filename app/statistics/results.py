from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.collection import Collection


@dataclass(slots=True)
class Statistics:

    total_cards: int
    unique_cards: int
    favorite_count: int
    wishlist_count: int
    most_owned: MostOwnedCard | None
    collection_value: float = 0


@dataclass(slots=True)
class ChartData:
    labels: list[str]
    values: list[int]


@dataclass(slots=True)
class CollectionType:

    type: str
    count: int


@dataclass(slots=True)
class CollectionRarity:

    rarity: str
    count: int


@dataclass(slots=True)
class MostOwnedCard:

    collection: "Collection"
    card_data: dict | None