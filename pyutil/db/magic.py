# -*- coding: utf-8 -*- 

import MySQLdb
import logging
import threading
import pyutil.common.sys_utf8
import pyutil.db.mysqlpool as mysqlpool
import re

class magic:

    def __init__(self, dbconfig):
        if not dbconfig:
            raise Exception("when call magic.__init__(self, db_config), db_config must not be None")
        self.__parse_config(dbconfig)

        self.pool = mysqlpool.mysqlpool(self.dbconfig, 4)


    def __parse_config(self, dbconfig):
        self.dbconfig = dbconfig
        alias = {"database":"db", "password":"passwd"}
        for k,v in alias.items():
            if self.dbconfig.get(k):
                self.dbconfig[v] = self.dbconfig[k]
                del self.dbconfig[k]
        self.dbconfig["connect_timeout"] = 3

    def __cursor_exec(self, cursor, lang):
        cursor.execute(lang)
        rows = cursor.fetchall()
        cursor.close()
        return rows
    
    def query_dict(self, lang):
        rows = [] 
        conn = self.pool.pop()
        try:

            cursor = conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
            rows = self.__cursor_exec(cursor, lang)

        except Exception, e:
            print "Error when query dict:",lang, "\n Exception:", e
            logging.error("Error when query dict: %s \n Exception: %s" %(lang, e))

        self.pool.push(conn)
        return rows

    def query(self, lang):
        rows = [] 
        conn = self.pool.pop()

        try:
            cursor = conn.cursor()
            rows = self.__cursor_exec(cursor, lang)
        except Exception, e:
            print "Error when query:",lang, "\n Exception:", e
            logging.error("Error when query: %s \n Exception: %s" %(lang, e))

        self.pool.push(conn)
        return rows
    
    def get_count(self, table_name): 
        lang = "SELECT COUNT(1) FROM " + table_name
        rows = self.query(lang)
        return int(rows[0][0]) if len(rows)>0 else 0

    def upsert(self, lang):
        rowcount, primaryid = -1, -1
        conn = self.pool.pop()

        try:
            cursor = conn.cursor()
            cursor.execute(lang)
            rowcount, primaryid = (cursor.rowcount, int(cursor.lastrowid)) if cursor.lastrowid else (-1,-1)
            cursor.close()
        except:
            print "Error when upsert sql:", lang
            logging.error("Error when upsert sql: %s" % lang)

        self.pool.push(conn)
        return rowcount, primaryid

    def execute_lang(self, lang, autocommit=False):
        rowcount, primaryid = -1, -1
        conn = self.pool.pop()

        try:
            cursor = conn.cursor()
            cursor.execute(lang.replace("\\", "\\\\"))
            rowcount, primaryid = (cursor.rowcount, int(cursor.lastrowid) if cursor.lastrowid else -1)
            
            if lang.upper().find("UPDATE ") == 0 and rowcount == 0:
                matchcount = self.__get_match_row_count(cursor._info)    
                rowcount = matchcount 

            if autocommit:
                conn.commit()

            cursor.close()
        except Exception, e:
            print "Error when execute_lang sql:", lang, ",exception：", e
            logging.error("Error when execute_lang sql: %s \n Exception: %s" %(lang, e))

        self.pool.push(conn)
        return rowcount, primaryid

    def execute(self, lang, params=(), autocommit=False):

        if not params:
            return self.execute_lang(lang, autocommit)

        rowcount, primaryid = -1, -1
        conn = self.pool.pop()
        try:
            cursor = self.conn.cursor()
            cursor.execute(lang, params)
            rowcount, primaryid = (cursor.rowcount, int(cursor.lastrowid) if cursor.lastrowid else -1)
            if lang.upper().find("UPDATE ") == 0 and rowcount == 0:
                matchcount = self.__get_match_row_count(cursor._info)    
                rowcount = matchcount 
            if autocommit:
                conn.commit()
            cursor.close()
        except Exception, e:
            print "Exception:", e, "Error when execute sql:", lang
            logging.error("Error when execute sql: %s \n Exception: %s" %(lang, e))

        self.pool.push(conn)
        return rowcount, primaryid
    
    def __get_match_row_count(self, _cursor_info):
        """获取执行SQL的匹配行数"""
        return int(re.search(r'Rows matched: (\d+)', _cursor_info).group(1))

def test():
    import pyconf.db.manna as manna
    mysql = magic(manna.config)
    rows = mysql.query_dict("SELECT * FROM info_user limit 1")
    for row in rows:
        print row

def test2():
    import pyconf.db.manna as manna
    mysql = magic(manna.config)
    ret = mysql.execute("insert into info_device_alarmer(alarmer_id, dtu_id, alarmer_no) values(123456789111, 12343, 123456789111)")
    print ret

    ret = mysql.execute("insert into info_device_alarmer(alarmer_id, dtu_id, alarmer_no) values(123456789111, 12343, 12345678)")
    print ret
    

if __name__ == '__main__':
    test2()
