from flask import Flask
from threading import Thread
from flask_restful import Resource, Api
from db.db import Db
import config.config as cfg
from updater.updater import new_proxy, checker

app = Flask(__name__)
api = Api(app)

proxy_thread = Thread(target=new_proxy, args=(), daemon=True)
check_thread = Thread(target=checker, args=(), daemon=True)
proxy_thread.start()
check_thread.start()

class ProxyProvider(Resource):
    def get(self):
        db = Db(cfg)
        return {'proxy':  db.select_proxy()}

api.add_resource(ProxyProvider, '/proxy')

if __name__ == '__main__':
    app.run(debug=True)

