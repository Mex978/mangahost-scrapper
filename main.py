from lib.scraping import mangahost
from lib import get_mangas
from lib import insert_manga_chapters
from lib import call_gcf_again
from time import time
from lib.config import Platforms
import json


def run(request):
    init = time()

    mangas = get_mangas.run(platform_type=Platforms.mangahosts)

    for manga in mangas:
        chapters = mangahost.scrap([manga], init)
        if chapters:
            insert_manga_chapters.run(chapters)
            # if time() - init >= 510:
            #     call_gcf_again.call()
            #     return "Continue execution"

    return "Finished"


run("apsodkaposkd")
