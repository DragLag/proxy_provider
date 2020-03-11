import pytest
from proxy_provider.db.db import Db
import proxy_provider.config.config as config
import os

class TestDb:
    def test_creat_db(self):
        db = Db(config)
        assert os.path.exists('proxy_list.db')

    def test_create_table(self):
        db = Db(config)
        db.create_table()
        row =db.cursor.execute("""
                       SELECT count(*) 
                       FROM sqlite_master 
                       WHERE type='table' AND name='proxies';
                       """).fetchone()
        assert row[0] == 1

    def test_insert_row(self):
        db = Db(config)
        db.insert_row(ipPort = "666.666.666.666")
        proxy = db.select_proxy()
        #print(proxy)
        db.delete_row('666.666.666.666')
        assert proxy == '666.666.666.666'
        #assert False

    def test_delete_row(self):
        db = Db(config)
        db.delete_row(ipPort = "666.666.666.666")
        proxy = db.select_proxy()
        print(proxy)
        assert proxy == False

    def test_tot_rows_no_rows(self):
        db = Db(config)
        n = db.tot_rows()
        assert n == 0

    def test_tot_rows(self):
        db = Db(config)
        db.insert_row(ipPort = "666.666.666.666")
        n = db.tot_rows()
        db.delete_row(ipPort = "666.666.666.666")
        assert n == 1
