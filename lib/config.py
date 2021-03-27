import os

TOKEN = os.getenv("TOKEN")
GCF_URL = os.getenv("GCF_URL")

BASE_URL = os.get("BASE_URL")
MANGAS_URL = f"{BASE_URL}/api/v1/mangas/"
CREATE_CHAPTER_URL = f"{BASE_URL}/api/v1/create-mangachapter/"