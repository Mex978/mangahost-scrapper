from lib.client.http import http
from lib import config


def run():
    token = config.TOKEN
    mangas_url = config.MANGAS_URL

    mangas = []

    response = http.get(
        mangas_url,
        headers={
            "Authorization": f"Token {token}",
        },
    )
    mangas_results = response.json().get("results")

    if mangas_results:
        mangas = [{"id": manga["id"], "title": manga["title"]} for manga in mangas_results]

    for manga in mangas:
        response = http.get(mangas_url + manga["id"], headers={"Authorization": f"Token {token}"})

        chapters_result = response.json()["chapters"]
        pt_chapters_result = [x for x in chapters_result if x["language"] == 1]

        pt_chapters_count = len(pt_chapters_result)
        manga["count"] = pt_chapters_count

    return mangas