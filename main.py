from logging import Logger
from lib import config
from lib.services.unifier_api_service import UnifierApiService
from lib.scraping.mangayabu import mangayabu
from lib.scraping.mangahost import mangahost
from lib.config import Platforms
from lib.client.http import http


def run(request=None):
    logger = config.logger
    platforms = [Platforms.mangayabu, Platforms.mangahosts]

    unifierApiService = UnifierApiService(http)

    mangahostClient = mangahost.Mangahost()
    mangayabuClient = mangayabu.Mangayabu()

    for platform in platforms:
        logger.warning(f"\n::> {platform} <::")
        logger.warning(f"Fetching mangas for {platform.value}\n")

        mangas = unifierApiService.getMangas(platform)

        for manga in mangas:
            chapters = (
                mangayabuClient.scrap(manga)
                if platform == Platforms.mangayabu
                else mangahostClient.scrap(manga)
            )

            if chapters:
                unifierApiService.insertChapter(chapters)

                # if time() - init >= 510:
                #     call_gcf_again.call()
                #     return "Continue execution"

    return "Finished"


run()
