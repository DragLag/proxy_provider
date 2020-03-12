import requests
import random
import config.config as cfg
import logging
import time
from db.db import Db


logging.basicConfig(filename='proxy_provider.log',
                    level=logging.INFO,
                    format='%(asctime)s %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p')
logger = logging.getLogger(__name__)

def new_proxy():
    print("new_proxy started")

    db = Db(cfg)
    while True:
        time.sleep(cfg.SLEEP_TIME)
        if db.tot_rows() <= cfg.MAX_IP:
            try:
                proxyjson = requests.get('http://gimmeproxy.com/api/getProxy?maxCheckPeriod=300?protocol=http').json()
                print(proxyjson)
            except requests.exceptions.RequestException as e:
                logger.error(e)
            except ValueError as e:  # includes simplejson.decoder.JSONDecodeError
                logger.error(e)
            if 'ipPort' in proxyjson.keys():
                db.insert_row(proxyjson['ipPort'])
                logger.info("proxy added: {}".format(proxyjson['ipPort']))
            else:
                logger.error(proxyjson)


def checker():
    print("checker started")
    db = Db(cfg)
    while True:
        time.sleep(cfg.SLEEP_TIME)
        ipPort = db.select_proxy()
        if ipPort:
            proxyDict = {
                "http": ipPort,
                "https": ipPort,
            }
            r = requests.get(cfg.LINK_TO_BE_CHECKED, headers={'User-Agent': random.choice(cfg.USER_AGENT)}, proxies=proxyDict)
            if not 200 <= r.status_code <= 299:
                db.delete_row(ipPort)
                logger.info("{} deleted".format(ipPort))
            else:
                logger.error("{} : {}".format(r.status_code, r.text))

