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
    most_owned_card: "Collection"
    most_owned_card_data: dict
    collection_value: float = 0
