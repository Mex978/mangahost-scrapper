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
        images_div = self.soup.find("div", class_="image-navigator")
        self.images = []

        for image in images_div.find_all("img"):
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
        self.logger.warning("Adicionado: {capitulo}".format(capitulo=self.title))
