import os
import requests


API_URL = "https://api.pokemontcg.io/v2/cards"

HEADERS = {
    "X-Api-Key": os.getenv("POKEMON_TCG_API_KEY")
}


def get_cards(search=None, page_size=50):
    search = search.strip()

    params = {
        "pageSize": page_size
    }

    if " " in search:
        params["q"] = f'name:"{search}"'
    else:
        params["q"] = f"name:*{search}*"

    print(params)

    response = requests.get(
        API_URL,
        headers=HEADERS,
        params=params
    )

    response.raise_for_status()

    return response.json()["data"]


def get_card(card_id: str):

    response = requests.get(
        url=API_URL + f"/{card_id}",
        headers=HEADERS
    )

    response.raise_for_status()

    print(response.json()["data"])

    return response.json()["data"]
