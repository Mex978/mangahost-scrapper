from logging import Logger
import os
from enum import Enum

TOKEN = os.getenv("TOKEN")
GCF_URL = os.getenv("GCF_URL")

BASE_URL = os.getenv("BASE_URL")
MANGAS_URL = f"{BASE_URL}/api/v1/mangas/"
PLATFORMS_URL = f"{BASE_URL}/api/v1/platform/"
CREATE_CHAPTER_URL = f"{BASE_URL}/api/v1/create-mangachapter/"

logger = Logger("scrapper")


class Platforms(Enum):
    mangahosts = "mangahost"
    isekaiscan = "isekaiscan"
    mangayabu = "mangayabu"
