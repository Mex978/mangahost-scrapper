import re
import sys
from time import sleep

from bs4 import BeautifulSoup
from bs4.element import Tag

from lib.client.http import http


def slugify(str):
    return "-".join(str.lower().split(" "))


def scrap(mangas):
    help = "Mangahost crawler command"
    platform = "https://mangahostz.com/"
    stdout = sys.stdout

    result = []

    for manga in mangas:
        sleep(1)

        manga_info = {}
        chapters_content = []

        manga_title = manga["title"]
        portuguese_chapters_count = manga["count"]

        stdout.write(f"Current manga: {manga}\n")

        response = http.get(f"{platform}manga/{slugify(manga_title)}")

        content = BeautifulSoup(response.text, "html.parser")

        manga_info = {**_find_manga_info(content)}

        chapters_div = content.find("div", {"class": "chapters"})
        chapter_item_divs = list(chapters_div.findChildren("div", recursive=False))
        chapter_item_divs = _remove_duplicates(chapter_item_divs)
        chapter_item_divs.reverse()
        manga_info["chapters_count"] = len(chapter_item_divs)

        if not _has_new_chapter(portuguese_chapters_count, manga_info["chapters_count"]):
            stdout.write(f"{manga} don't have any new chapters\n")
            continue

        limit = _find_chapter_interval(portuguese_chapters_count, manga_info["chapters_count"])
        limit = abs(manga_info["chapters_count"] - limit)

        for chapter_item_div in chapter_item_divs[limit:]:
            data = _find_chapter_info(chapter_item_div, manga)
            stdout.write(f"Chapter: {data}\n")

            response = http.get(data["url"])
            content = BeautifulSoup(response.text, "html.parser")

            data["images"] = _find_chapter_images(content)

            del data["url"]

            sleep(1)

            chapters_content.append(data)

        result.append({"info": manga_info, "chapters": chapters_content})

    return result


def _has_new_chapter(portuguese_chapters_count: int, chapters_count: int) -> bool:
    if chapters_count <= portuguese_chapters_count:
        return False
    return True


def _find_manga_info(content: BeautifulSoup) -> dict:
    _manga_info = {}

    box_info = content.find("div", {"class": "box-content alert alert-left w-row"})
    summary_image = content.find("div", {"class": "widget"})
    tags_field = content.find_all("a", {"class": "tag"})
    description_field = content.find("div", {"class": "paragraph"})

    info_items_uls = box_info.find_all("ul", {"class": "w-list-unstyled"})
    for info_item_ul in info_items_uls:
        info_item_divs = info_item_ul.find_all("div")

        for info_item_div in info_item_divs:
            content = info_item_div.text
            content_splitted = content.split(":")

            title = content_splitted[0].strip().lower()
            text = content_splitted[1].strip()

            if title == "autor":
                _manga_info["author"] = text
            elif title == "status":
                _manga_info["status"] = text

    _manga_info["tags"] = [tag.text.capitalize() for tag in tags_field]
    _manga_info["description"] = description_field.find("p").text

    return _manga_info


def _find_chapter_info(element: Tag, manga) -> dict:
    data = {}

    url = element.find("a", {"class": "btn-green w-button pull-left"}).attrs["href"]
    number = url.split("/")[-1]

    data["title"] = element.find("div", {"class": "pop-title"}).text
    data["number"] = int(re.findall(r"\d+", number)[0])
    data["language"] = "PORTUGUESE_BR"
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
