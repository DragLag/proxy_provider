from config import DB_NAME
import sqlite3
import os

class Db:
    def __main__(self):
        if not os.path.exists(DB_NAME):
            self.cursor = self.create_db_connection()
            self.create_table()
        else:
            self.cursor = self.create_db_connection()


    def create_db_connection(self):
        """ create a database connection to a SQLite database """
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = self.conn.cursor()
        except Exception as e:
            logger.error(e)
        return cursor

    def create_table(self):
        create_table = """ 
                       CREATE TABLE IF NOT EXISTS proxies (
                       id integer PRIMARY KEY,
                       ipPort text NOT NULL,
                       );
                        """
        try:
            self.cursor.execute(create_table)
        except Exception as e:
            logger.error(e)

    def insert_row(self, ipPort):
        insert_proxy = """
                          INSERT INTO proxies(ipPort)
                          VALUES( ?,  ?);
                           """
        try:
            self.cursor.execute(insert_proxy, (ipPort))
            logger.debug("proxy {0} inserted in db ".format(self.address['ipPort']))
        except Exception as e:
            logger.error(e)


    def delete_row(self, ipPort):
        delete_row = """
                       DELETE 
                       FROM proxies
                       WHERE ipPort = ?
                       """
        try:
            self.cursor.execute(delete_row, (ipPort))
            logger.debug("proxy {0} deleted ".format(ipPort))
        except Exception as e:
            logger.error(e)
