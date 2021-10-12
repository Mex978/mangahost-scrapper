from lib import config
import re
import requests

from bs4 import BeautifulSoup


class Chapter:
    def __init__(self, title, url, manga_title):
        self.logger = config.logger

        self.title = title
        self.url = url
        self.manga_title = manga_title
        self.language = 1
        self.number = int(re.findall(r"\d+", self.title)[0])

        self.addRequest()
        self.addSoup()
        self.addImagensUrls()
        self.show()

    def addRequest(self):
        self.request = requests.get(self.url)

    def addSoup(self):
        self.soup = BeautifulSoup(self.request.text, "html.parser")

    def addImagensUrls(self):
        self.images = []

        def is_chapter_image(element):
            if (
                element
                and element.find(self.manga_title) != -1
                and element.find("Capítulo") != -1
            ):
                return True

            return False

        imgs = self.soup.find_all("img", {"title": is_chapter_image})

        for image in imgs:
            self.images.append(image.attrs["src"])

    def getImagensUrls(self):
        return self.images

    def getTitle(self):
        return self.title

    def getJson(self):
        return {
            "title": self.title,
            "manga": self.manga_title,
            "language": self.language,
            "number": self.number,
            "images": self.images,
        }

    def show(self):
        self.logger.warning(f"Adicionado: {self.title}")
