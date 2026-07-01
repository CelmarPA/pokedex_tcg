from dataclasses import dataclass
from .pagination import Pagination


@dataclass(slots=True)
class CardSearchResult:
    cards: list
    pagination: Pagination