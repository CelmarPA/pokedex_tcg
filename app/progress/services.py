from ..cards.services import get_card



def get_collection_progress(user):
    progress = {}

    for item in user.collections:
        card = get_card(item.card_id)

        set_id = card["set"]["id"]

        if set_id not in progress:
            progress[set_id] = {
                "set_id": set_id,
                "set_name": card["set"]["name"],
                "series": card["set"]["series"],
                "owned": 0,
                "total": card["set"]["printedTotal"]
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
