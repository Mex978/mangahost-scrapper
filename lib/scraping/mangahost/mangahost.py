from lib import config
from logging import Logger
from time import sleep

from lib.helpers.functions import Functions
from lib.scraping.mangahost.manga import Manga


class Mangahost:
    def __init__(self, init_time=None) -> None:
        self._init_time = init_time
        self.logger = config.logger

        self._help = "Mangahost crawler command"
        self._platform = "https://mangahostz.com/"

    def scrap(self, manga):
        result = []

        attempts = 3
        while attempts > 0:
            _id = manga["id"]
            _title = manga["title"]
            _count = manga["count"]
            _url = self._platform + "manga/" + Functions.slugify(_title)

            try:
                self.logger.warning(f"Current manga: {_title}")
                _manga = Manga(id=_id, title=_title, count=_count, url=_url)

                if _manga.chapters:
                    result += _manga.chapters

                attempts = 0
                sleep(2)
            except Exception as e:
                attempts -= 1
                self.logger.warning(f"\t--> Error on {_title} - {e}")
                sleep(3)

        return result
