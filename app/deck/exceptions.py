class DeckError(Exception):
    """Base exception for the deck module."""


class DeckNotFoundError(DeckError):
    """Deck not found."""

    def __init__(self):
        super().__init__("Deck not found.")


class DeckCardNotFoundError(DeckError):
    """Card not found in deck."""

    def __init__(self):
        super().__init__("Card not found in deck.")


class DeckValidationError(DeckError):
    """Deck validation failed."""


class DeckRuleError(DeckError):
    """Official Pokémon TCG deck rule violation."""

    def __init__(self, message):
        super().__init__(message)
