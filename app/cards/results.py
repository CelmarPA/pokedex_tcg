from dataclasses import dataclass
from ..models import Collection, Favorite, Wishlist


@dataclass(slots=True)
class CardDetail:

    card_data: dict | None
    prices: MarketPrices | None
    collection_card: Collection | None
    favorite_card: Favorite | None
    cards_wishlist: Wishlist | None


@dataclass(slots=True)
class MarketPrices:

    market_name: str = ""
    market_url: str = ""
    market: float = 0
    low: float = 0
    mid: float = 0
    high: float = 0
    market_label: str = "Market"
    mid_label: str = "Mid"
    high_label: str = "High"
