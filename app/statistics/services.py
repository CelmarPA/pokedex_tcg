# app/statistics/services.py
from ..cards.services import get_card


def get_user_statistics(user):
    total_cards = sum(card.quantity for card in user.collections)

    unique_cards = len(user.collections)

    favorite_count = len(user.favorites)

    wishlist_count = len(user.wishlists)

    most_owned_card = None
    most_owned_card_data = None

    collection_value = 0

    if user.collections:
        most_owned_card = max(
            user.collections,
            key=lambda card: card.quantity
        )

        if most_owned_card:
            most_owned_card_data = get_card(most_owned_card.card_id)

        for item in user.collections:
            card_data = get_card(item.card_id)

            tcgplayer = card_data.get("tcgplayer")

            if not tcgplayer:
                continue

            prices = tcgplayer.get("prices", {})

            card_type_dict = prices.get("holofoil") or prices.get("normal")

            market_price = card_type_dict.get("market", 0) if card_type_dict else 0

            collection_value += (market_price * item.quantity)

    return {
        "total_cards": total_cards,
        "unique_cards": unique_cards,
        "favorite_count": favorite_count,
        "wishlist_count": wishlist_count,
        "most_owned_card": most_owned_card,
        "most_owned_card_data": most_owned_card_data,
        "collection_value": collection_value
    }
