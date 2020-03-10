import requests
from config import LINK_TO_BE_CHECKED, USER_AGENT
import random
from flask import Flask, jsonify
from threading import Thread
#from tasks import threaded_task
from flask_restful import Resource, Api
from db.db import Db
from config import MAX_IP, SLEEP_TIME
import time
import logging

logging.basicConfig(filename='proxy_provider.log',
                    level=logging.INFO,
                    format='%(asctime)s %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p')
logger = logging.getLogger(__name__)

db = Db()

def new_proxy():
    print("new_proxy started")
    while True:
        time.sleep(SLEEP_TIME)
        if db.tot_rows() <= MAX_IP:
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
    while True:
        time.sleep(SLEEP_TIME)
        ipPort = db.select_proxy()
        if not ipPort:
           continue
        proxyDict = {
            "http": ipPort,
            "https": ipPort,
        }
        r = requests.get(LINK_TO_BE_CHECKED, headers={'User-Agent': random.choice(USER_AGENT)}, proxies=proxyDict)
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
        return {'proxy':  db.select_proxy()}

api.add_resource(ProxyProvider, '/proxy')

if __name__ == '__main__':
    app.run(debug=True)

