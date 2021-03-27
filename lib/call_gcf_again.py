from lib import config
import requests


def call():
    try:
        target_audience = config.GCF_URL
        print(target_audience)

        requests.get(target_audience, timeout=0.001)
    except:
        pass
