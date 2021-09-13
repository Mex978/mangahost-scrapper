import re
from bs4 import BeautifulSoup

from lib import config
from lib.client.http import http
from lib.services.unifier_api_service import UnifierApiService
from lib.scraping.mangayabu.chapter import Chapter


class Manga:
    def __init__(self, id, url, title, count):
        self.apiService = UnifierApiService(http)
        self.logger = config.logger

        self.id = id
        self.title = title
        self.portuguese_chapters_count = count
        self.url = url

        self.addRequest()
        self.addSoup()
        self.addChapters()

    def addRequest(self):
        self.request = http.get(self.url)

    def addSoup(self):
        self.soup = BeautifulSoup(self.request.text, "html.parser")

    def addChapters(self):
        chapters_divs = self.soup.findAll("div", class_="single-chapter")
        chapters_divs.reverse()

        chapters_count = len(chapters_divs)

        self.chapters = []

        if not self._has_new_chapter(chapters_count):
            self.logger.warning(f"{self.title} don't have any new chapters")
            self.apiService.updateMangaChaptersCount(
                self.id,
                self.portuguese_chapters_count,
            )
            return

        limit = self._find_chapter_interval(chapters_count)
        limit = abs(chapters_count - limit)

        for div in chapters_divs[limit:]:
            if len(re.findall(r"\d+", div.a.text)) > 0:
                capitulo = Chapter(div.a.text, div.a["href"], self.title)
                self.chapters.append(capitulo.getJson())

        self.apiService.updateMangaChaptersCount(
            self.id,
            chapters_count,
        )

    def getChapters(self):
        return self.chapters

    def _has_new_chapter(self, chapters_count: int) -> bool:
        return self.portuguese_chapters_count < chapters_count

    def _find_chapter_interval(self, chapters_count: int) -> int:
        if self.portuguese_chapters_count == 0:
            return chapters_count
        return abs(self.portuguese_chapters_count - chapters_count)
