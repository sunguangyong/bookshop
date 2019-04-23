#!/usr/local/bin/python
# -*- coding: utf8 -*-  
  
''' 
Created on 2017-11-23 
@author: basearch@fubangyun.com
'''  

import MySQLdb
import logging
import time
import threading

class mysqlpool():
    def __init__(self, config, max_num):
        self.dbconfig = config
        self.con_map = {}
        self.Lock = threading.Lock()

        try:
            for i in range(0, max_num):
                self.con_map[self.connect()] = 0
        except Exception as e:    
            logging.warning(e)

    def connect(self):
        conn = MySQLdb.connect(**self.dbconfig)
        if not conn:
            raise Exception("Error: magic.reconnect, self.conn is None")

        conn.autocommit(True)

        cursor = conn.cursor()
        cursor.execute("set session transaction isolation level read committed;")
        cursor.close()

        return conn


    def __get_free_conn(self):
        self.Lock.acquire()
        for c in self.con_map:
            if self.con_map[c] == 0:
                self.con_map[c] = 1

                self.Lock.release() 
                return c

        self.Lock.release() 
        return None


    def __get_refreshed_conn(self, conn):
        self.Lock.acquire()

        if conn in self.con_map:
            del self.con_map[conn]

        conn = self.connect()
        self.con_map[conn] = 1

        self.Lock.release() 
        return conn


    def pop(self):
        while 1:
            conn = self.__get_free_conn()
            if not conn:
                print "Warnning, get a free connection, will retry after waiting 0.1s, host:port=", self.dbconfig["host"]+":"+str(self.dbconfig["port"])
                time.sleep(0.1)     
            else:
                break

        try:
            conn.ping(True)
            return conn
        except MySQLdb.OperationalError,e:
            print "Warning: connection refresh"
            return self.__get_refreshed_conn(conn)


    def push(self, conn):
        self.Lock.acquire() 
        self.con_map[conn] = 0
        self.Lock.release() 


if __name__ == '__main__':
    import db_example
    pool = mysqlpool(db_example.config)
    con = pool.get_conn()
    cursor = con.cursor()
    print dir(cursor)
    cursor.execute("SELECT id, name FROM users WHERE id = 1")
    rows = cursor.fetchall()
    for row in rows:
        print row[0], row[1]
