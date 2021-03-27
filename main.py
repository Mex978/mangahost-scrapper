from lib.scraping import mangahost
from lib import get_mangas
from lib import insert_manga_chapters
import json


def run(request):
    mangas = get_mangas.run()

    chapters = mangahost.scrap(mangas)
    if chapters:
        insert_manga_chapters.run(chapters)
