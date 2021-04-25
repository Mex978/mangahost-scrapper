from lib.client.http import http
from lib import config


def run(platform_type: config.Platforms):
    token = config.TOKEN
    platforms_url = config.PLATFORMS_URL
    mangas_url = config.MANGAS_URL

    mangas = []

    response = http.get(
        platforms_url,
        headers={
            "Authorization": f"Token {token}",
        },
    )
    platform_results = response.json().get("results")

    for platform in platform_results:
        if platform["name"] == platform_type.value:
            mangas = platform["mangas"]

            for manga in mangas:
                response = http.get(mangas_url + manga["id"], headers={"Authorization": f"Token {token}"})

                chapters_result = response.json()["chapters"]
                pt_chapters_result = [x for x in chapters_result if x["language"] == 1]

                pt_chapters_count = len(pt_chapters_result)
                manga["count"] = pt_chapters_count

            return mangas
