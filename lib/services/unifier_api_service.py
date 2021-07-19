import json
from lib import config


class UnifierApiService:
    def __init__(self, unifier_api_client):
        self._unifier_api_client = unifier_api_client
        self._token = config.TOKEN
        self._platforms_url = config.PLATFORMS_URL
        self._mangas_url = config.MANGAS_URL

    def getMangas(self, platform_type: config.Platforms):
        mangas = []

        response = self._unifier_api_client.get(
            self._platforms_url,
            headers={
                "Authorization": f"Token {self._token}",
            },
        )
        platform_results = response.json().get("results")

        for platform in platform_results:
            if platform["name"] == platform_type.value:
                mangas = platform["mangas"]

                for manga in mangas:
                    response = self._unifier_api_client.get(
                        self._mangas_url + manga["id"],
                        headers={"Authorization": f"Token {self._token}"},
                    )

                    chapters_result = response.json()["chapters"]
                    pt_chapters_result = [
                        x for x in chapters_result if x["language"] == 1
                    ]

                    pt_chapters_count = len(pt_chapters_result)
                    manga["count"] = pt_chapters_count

                return mangas

    def insertChapter(self, chapters):
        create_chapter_url = config.CREATE_CHAPTER_URL

        self._unifier_api_client.post(
            create_chapter_url,
            data=json.dumps(chapters),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Token {self._token}",
            },
        )

    def updateMangaChaptersCount(self, manga_id, count):
        self._unifier_api_client.patch(
            self._mangas_url + manga_id + "/",
            data={
                "chapters_count": count,
            },
            headers={
                "Authorization": f"Token {self._token}",
            },
        )
