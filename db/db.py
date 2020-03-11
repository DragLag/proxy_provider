import sqlite3
import os
import logging


logging.basicConfig(filename='proxy_provider.log',
                    level=logging.INFO,
                    format='%(asctime)s %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p')
logger = logging.getLogger(__name__)

class Db:
    def __init__(self, config):
        self.cursor = self.create_db_connection(config.DB_NAME)
        if not os.path.exists(config.DB_NAME):
            self.create_table()


    def create_db_connection(self, DB_NAME):
        """ create a database connection to a SQLite database """
        try:
            conn = sqlite3.connect(DB_NAME)
        except Exception as e:
            logger.error(e)
        return conn.cursor()

    def create_table(self):
        create_table = """ 
                       CREATE TABLE IF NOT EXISTS proxies (
                       id integer PRIMARY KEY,
                       ipPort text NOT NULL
                       );
                        """
        try:
            self.cursor.execute(create_table)
        except Exception as e:
            logger.error(e)

    def insert_row(self, ipPort):
        insert_proxy = """
                          INSERT INTO proxies(ipPort)
                          VALUES(?);
                           """
        try:
            self.cursor.execute(insert_proxy, (ipPort,))
            logger.debug("proxy {0} inserted in db ".format(ipPort))
        except Exception as e:
            logger.error(e)


    def delete_row(self, ipPort):
        delete_row = """
                       DELETE 
                       FROM proxies
                       WHERE ipPort = ?
                       """
        try:
            self.cursor.execute(delete_row, (ipPort,))
            logger.debug("proxy {0} deleted ".format(ipPort))
        except Exception as e:
            logger.error(e)

    def tot_rows(self):
        tot_rows = """
                      SELECT COUNT(*)
                      FROM proxies
                      """
        try:
            rows = self.cursor.execute(tot_rows).fetchone()
        except Exception as e:
            logger.error(e)
        return rows[0]

    def select_proxy(self):
        select_proxy = """
                          SELECT ipPort FROM proxies
                          ORDER BY random() limit 1 
                           """
        try:
            self.cursor.execute(select_proxy)
            proxy = self.cursor.fetchone()[0]
        except Exception as e:
            logger.error(e)
            return False
        return proxy
