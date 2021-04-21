import re
import sys
from time import sleep, time

from bs4 import BeautifulSoup
from bs4.element import Tag

from lib.client.http import http


def slugify(str):
    str = str.replace("’", "").replace("!", "").replace("?", "")

    return "-".join(str.lower().split(" "))


def scrap(mangas, init_time):
    help = "Mangahost crawler command"
    platform = "https://mangahostz.com/"
    stdout = sys.stdout

    result = []

    for manga in mangas:
        try:
            chapters_content = _get_manga_chapters(stdout, platform, manga)
            if chapters_content:
                result += chapters_content
        except Exception as e:
            stdout.write(f"Error on {manga} - {e}")

    return result


def _get_manga_chapters(stdout, platform, manga):
    sleep(1)

    chapters_content = []

    manga_title = manga["title"]
    portuguese_chapters_count = manga["count"]

    stdout.write(f"Current manga: {manga_title}\n")

    response = http.get(f"{platform}manga/{slugify(manga_title)}")
    content = BeautifulSoup(response.text, "html.parser")

    chapters_div = content.find("div", {"class": "chapters"})
    chapter_item_divs = list(chapters_div.findChildren("div", recursive=False))
    chapter_item_divs = _remove_duplicates(chapter_item_divs)
    chapter_item_divs.reverse()

    manga_chapters_count = len(chapter_item_divs)

    if not _has_new_chapter(portuguese_chapters_count, manga_chapters_count):
        stdout.write(f"{manga_title} don't have any new chapters\n")
        return None

    limit = _find_chapter_interval(portuguese_chapters_count, manga_chapters_count)
    limit = abs(manga_chapters_count - limit)

    for chapter_item_div in chapter_item_divs[limit:]:
        if (time() - init_time) >= 510:
            stdout.write(f"Timeout for {manga_title}")
            return chapters_content

        data = _find_chapter_info(chapter_item_div, manga_title)
        stdout.write(f"Chapter: {data}\n")

        response = http.get(data["url"])
        content = BeautifulSoup(response.text, "html.parser")

        data["images"] = _find_chapter_images(content)

        del data["url"]

        sleep(1)

        chapters_content.append(data)

    return chapters_content


def _has_new_chapter(portuguese_chapters_count: int, chapters_count: int) -> bool:
    if chapters_count <= portuguese_chapters_count:
        return False
    return True


def _find_chapter_info(element: Tag, manga) -> dict:
    data = {}

    url = element.find("a", {"class": "btn-green w-button pull-left"}).attrs["href"]
    number = url.split("/")[-1]

    data["title"] = element.find("div", {"class": "pop-title"}).text
    data["number"] = int(re.findall(r"\d+", number)[0])
    data["language"] = 1
    data["manga"] = manga
    data["url"] = url
    data["images"] = []

    return data


def _find_chapter_images(content: BeautifulSoup) -> list:
    images_div = content.find("div", {"id": "slider"})
    return [image.attrs["src"].strip() for image in images_div.find_all("img")]


def _find_chapter_interval(portuguese_chapters_count: int, chapters_count: int) -> int:
    if portuguese_chapters_count == 0:
        return chapters_count
    return abs(portuguese_chapters_count - chapters_count)


def _remove_duplicates(items: list) -> list:
    _new_items = []
    _urls = []

    for item in items:
        _url = item.find("a", {"class": "btn-green w-button pull-left"}).attrs["href"]

        if _url not in _urls:
            _urls.append(_url)
            _new_items.append(item)

    return _new_items
