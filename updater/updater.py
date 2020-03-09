import requests
from config import LINK_TO_BE_CHECKED, USER_AGENT
import random
class Updater:

    def new_proxy(self, link):
        try:
            proxyjson = requests.get('http://gimmeproxy.com/api/getProxy?maxCheckPeriod=300?protocol=http').json()
        except requests.exceptions.RequestException as e:
            logger.error(e)
        except ValueError as e:  # includes simplejson.decoder.JSONDecodeError
            logger.error(e)
        if 'ipPort' in proxyjson.keys():
            logger.debug('ipPort in json')
        return proxyjson['ipPort']

    def check_proxy(self, ipPort):
        proxyDict = {
            "http": ipPort,
            "https": ipPort,
        }
        r = requests.get(LINK_TO_BE_CHECKED, headers={'User-Agent': random.choice(USER_AGENT)}, proxies=proxyDict)

