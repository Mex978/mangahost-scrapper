from lib.scraping import mangahost
from lib import get_mangas
from lib import insert_manga_chapters
from lib import call_gcf_again
from time import time
import json


def run(request):
    init = time()

    mangas = get_mangas.run()

    for manga in mangas:
        chapters = mangahost.scrap([manga], init)
        if chapters:
            print(chapters)

            insert_manga_chapters.run(chapters)
            if time() - init >= 530:
                call_gcf_again.call()
                print("END TIME")
                break
