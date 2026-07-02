from dataclasses import dataclass


@dataclass(slots=True)
class CollectionProgress:

    set_id: str
    set_name: str
    series: str
    owned: int
    total: int
    symbol: str
    logo: str
    progress: float = 0


@dataclass(slots=True)
class CollectionCard:

    card: dict
    quantity: int

