from ..cards.services import get_card_smart


def get_collection_value(user):

    collection_value = 0

    for item in user.collections:
        card_data = get_card_smart(item.card_id)

        tcgplayer = card_data.get("tcgplayer")

        if not tcgplayer:
            continue

        prices = tcgplayer.get("prices", {})

        card_type_dict = prices.get("holofoil") or prices.get("normal")

        market_price = card_type_dict.get("market", 0) if card_type_dict else 0

        collection_value += (market_price * item.quantity)

    return collection_value


def get_collection_progress(user):
    progress = {}

    for item in user.collections:
        card = get_card_smart(item.card_id)

        set_id = card["set"]["id"]

        set_images = card["set"]["images"]

        if set_id not in progress:
            progress[set_id] = {
                "set_id": set_id,
                "set_name": card["set"]["name"],
                "series": card["set"]["series"],
                "owned": 0,
                "total": card["set"]["printedTotal"],
                "symbol": set_images["symbol"],
                "logo": set_images["logo"]
            }


        progress[set_id]["owned"] += 1

    for set_data in progress.values():

        set_data["progress"] = round(
            (set_data["owned"] / set_data["total"]) * 100,
            1
        )

    return sorted(
        progress.values(),
        key=lambda x: x["progress"],
        reverse=True
    )
