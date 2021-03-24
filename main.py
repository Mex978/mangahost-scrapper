from lib import mangahost


def run(request):
    mangas = [
        {
            "title": "The beginning after the end",
            "count": 94,
        },
    ]

    mangas = mangahost.scrap(mangas)

    for manga in mangas:
        print(manga["info"])

        for chapter in manga["chapters"]:
            print(chapter)

    return mangas