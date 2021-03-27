import os

TOKEN = os.getenv("TOKEN")

BASE_URL = "http://manga-unifier.herokuapp.com"
MANGAS_URL = f"{BASE_URL}/api/v1/mangas/"
CREATE_CHAPTER_URL = f"{BASE_URL}/api/v1/create-mangachapter/"