from dataclasses import dataclass
from ..models import Collection, Favorite, Wishlist


@dataclass(slots=True)
class CardDetail:

    card_data: dict | None
    prices: dict | None
    collection_card: Collection | None
    favorite_card: Favorite | None
    cards_wishlist: Wishlist | None


@dataclass(slots=True)
class MarketPrices:

    market: float
    low: float
    mid: float
    high: float