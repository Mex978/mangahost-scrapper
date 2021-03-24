from lib import mangahost
import json 


def run(request):
    mangas = [
        {
            "title": "The beginning after the end",
            "count": 94,
        },
    ]

    mangas = mangahost.scrap(mangas)

    return json.dumps(mangas)