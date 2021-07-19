from lib.client.http import http
from lib import config
import json


def run(chapters):
    token = config.TOKEN
    create_chapter_url = config.CREATE_CHAPTER_URL

    http.post(
        create_chapter_url,
        data=json.dumps(chapters),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Token {token}",
        },
    )
