from lib import config
from lib.helpers.functions import Functions
from lib.scraping.mangayabu.manga import Manga


class Mangayabu:
    def __init__(self, init_time=None) -> None:
        self._init_time = init_time
        self.logger = config.logger

        self._help = "Mangayabu crawler command"
        self._platform = "https://mangayabu.top/"

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

            except Exception as e:
                attempts -= 1
                self.logger.warning(f"\t--> Error on {_title} - {e}")

        return result
