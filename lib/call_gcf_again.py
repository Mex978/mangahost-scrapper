from lib import config
import requests


def call():
    try:
        target_audience = config.GCF_URL
        requests.post(target_audience, timeout=5)
    except:
        pass
