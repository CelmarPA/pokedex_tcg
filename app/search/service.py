from .constants import (
    CARD_TYPES,
    CARD_SUPERTYPES,
    CARD_RARITIES
)


class SearchService:

    def __init__(self):
        self.card_types = CARD_TYPES
        self.card_supertypes = CARD_SUPERTYPES
        self.card_rarities = CARD_RARITIES

    def build_query(self, filters):

        query = []

        # Search by name
        if filters.search:

            if " " in filters.search:
                query.append(f'name:"{filters.search}"')

            else:
                query.append(f"name:*{filters.search}*")

        # Filter by type
        if filters.type:
            query.append(f'types:"{filters.type}"')

        # Filter by rarity
        if filters.rarity:
            query.append(f'rarity:"{filters.rarity}"')

        # Filter by supertype
        if filters.supertype:
            query.append(f'supertype:"{filters.supertype}"')

        return " ".join(query)

    def get_filters(self):

        return {
            "types": self.card_types,
            "rarities": self.card_rarities,
            "supertypes": self.card_supertypes
        }

    def get_search_context(self, ):

        return {
            "filter_options": self.get_filters()
        }

    def match_search(self, search, text):

        if not search:
            return True

        return search.casefold() in text.casefold()

    def match_filters(self, filters, card):

        if not self.match_search(filters.search, card["name"]):
            return False

        if filters.type and filters.type not in card.get("types", []):
            return False

        if filters.rarity and card.get("rarity") != filters.rarity:
            return False

        if filters.supertype and card.get("supertype") != filters.supertype:
            return False

        return True


search_service = SearchService()