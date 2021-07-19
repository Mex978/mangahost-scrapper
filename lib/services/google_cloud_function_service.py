from lib import config
import requests


class GCloudFunctionService:
    def __init__(self):
        pass

    def call_function(self):
        try:
            target_audience = config.GCF_URL
            requests.post(target_audience, timeout=5)
        except:
            pass
