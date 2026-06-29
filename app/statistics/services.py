# app/statistics/services.py
from collections import defaultdict, Counter
from ..cards.services import get_card_smart
from ..collection.services import get_collection_value


def get_user_statistics(user):

    total_cards = sum(card.quantity for card in user.collections)

    unique_cards = len(user.collections)

    favorite_count = len(user.favorites)

    wishlist_count = len(user.wishlists)

    most_owned_card = None
    most_owned_card_data = None

    collection_value = get_collection_value(user)

    if user.collections:

        most_owned_card = max(
            user.collections,
            key=lambda card: card.quantity
        )

        if most_owned_card:
            most_owned_card_data = get_card_smart(most_owned_card.card_id)

    return {
        "total_cards": total_cards,
        "unique_cards": unique_cards,
        "favorite_count": favorite_count,
        "wishlist_count": wishlist_count,
        "most_owned_card": most_owned_card,
        "most_owned_card_data": most_owned_card_data,
        "collection_value": collection_value
    }


def get_collection_progress(user):

    sets = defaultdict(dict)

    for item in user.collections:

        card = get_card_smart(item.card_id)

        set_data = card["set"]

        set_id = set_data["id"]

        if set_id not in sets:
            sets[set_id] = {
                "set_id": set_id,
                "set_name": set_data["name"],
                "symbol": set_data["images"]["symbol"],
                "logo": set_data["images"]["logo"],
                "owned": 0,
                "total": set_data["printedTotal"]
            }

        sets[set_id]["owned"] += 1

    progress = []

    for set_info in sets.values():

        set_info["progress"] = round(
            (set_info["owned"] / set_info["total"]) * 100,
            1
        )

        progress.append(set_info)

    progress.sort(
        key=lambda s: s["progress"],
        reverse=True
    )

    return progress


def get_favorite_types(user):

    types = Counter()

    for item in user.collections:

        card = get_card_smart(item.card_id)

        for pokemon_type in card.get("types", []):

            types[pokemon_type] += item.quantity

    return [
        {
            "type": pokemon_type,
            "count": count
        }
        for pokemon_type, count in types.most_common()
    ]


def get_collection_rarity(user):

    rarities = Counter()

    for item in user.collections:

        card = get_card_smart(item.card_id)

        rarity = card.get("rarity", "Unknown")

        rarities[rarity] += item.quantity

    return [
        {
            "rarity": rarity,
            "count": count
        }
        for rarity, count in rarities.most_common()
    ]
