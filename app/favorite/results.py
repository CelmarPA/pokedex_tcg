from dataclasses import dataclass


@dataclass(slots=True)
class ToggleResult:

    added: bool


@dataclass(slots=True)
class FavoriteCard:

    card: dict
