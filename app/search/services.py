from .contants import (
    CARD_TYPES,
    CARD_SUPERTYPES,
    CARD_RARITIES
)


def build_query(filters):

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


def get_filters():

    return {
        "types": CARD_TYPES,
        "rarities": CARD_RARITIES,
        "supertypes": CARD_SUPERTYPES
    }


def get_search_context():

    return {
        "filter_options": get_filters()
    }
