import requests
import random
from flask import Flask, jsonify
from threading import Thread
#from tasks import threaded_task
from flask_restful import Resource, Api
from db.db import Db
import config.config as cfg
import time
import logging

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
            except requests.exceptions.RequestException as e:
                logger.error(e)
            except ValueError as e:  # includes simplejson.decoder.JSONDecodeError
                logger.error(e)
            if 'ipPort' in proxyjson.keys():
                db.insert_row(proxyjson['ipPort'])


def checker():
    print("checker started")
    db = Db(cfg)
    while True:
        time.sleep(cfg.SLEEP_TIME)
        ipPort = db.select_proxy()
        if not ipPort:
           continue
        proxyDict = {
            "http": ipPort,
            "https": ipPort,
        }
        r = requests.get(cfg.LINK_TO_BE_CHECKED, headers={'User-Agent': random.choice(cfg.USER_AGENT)}, proxies=proxyDict)
        if not 200 <= r.status_code <= 299:
            db.delete_row(ipPort)


app = Flask(__name__)
api = Api(app)

#proxy_thread = Thread(target=new_proxy, args=(), daemon=True)
#check_thread = Thread(target=checker, args=(), daemon=True)
#proxy_thread.start()
#check_thread.start()

@app.route('/')
def index():
    proxy_thread = Thread(target=new_proxy, args=(), daemon=True)
    check_thread = Thread(target=checker, args=(), daemon=True)
    proxy_thread.start()
    check_thread.start()
    return jsonify({'proxy_provider': 'started'})

class ProxyProvider(Resource):
    def get(self):
        db = Db(cfg)
        return {'proxy':  db.select_proxy()}

api.add_resource(ProxyProvider, '/proxy')

if __name__ == '__main__':
    app.run(debug=True)

