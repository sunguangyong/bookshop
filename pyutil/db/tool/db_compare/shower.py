# -*- coding: utf-8 -*-

import pyutil.common.sys_utf8 as sys_utf8
import pyutil.db.magic as magic
import pyutil.db.util as db_util
import re
import json
import difflib
import datetime

enum_re = "^enum|^hz_|^pt_|info_sense_type|^vid_"


class Shower:
    def __init__(self, config_A, config_B, ignores=[]):
        self.lacks, self.more, self.common = [], [], []
        self.mysql_a = magic.magic(config_A)
        self.mysql_b = magic.magic(config_B)

        self.ignores = ignores

    def diff(self, list_a, list_b):
        more = [a for a in [a for a in list_a if a not in list_b ] if a not in self.ignores]
        common = [a for a in [a for a in list_a if a in list_b ] if a not in self.ignores]
        lacks = [b for b in [b for b in list_b if b not in list_a] if b not in self.ignores]
        return more, common, lacks

    def same(self, list_a, list_b):
        return sorted(list_a) == sorted(list_b)

    def create_sql(self, mysql, tables):
        for t in tables:
            rows = mysql.query("SHOW CREATE TABLE `%s`" % (t))
            print "%s;\n" % (rows[0][1])
        else:
            print "无"

    def run(self):
        tables_a = [row[0] for row in self.mysql_a.query("SHOW TABLES")]
        tables_b = [row[0] for row in self.mysql_b.query("SHOW TABLES")]
        more, common, lacks = self.diff(tables_a, tables_b)
        print ">>>>>>>>>>>>>>>>>>>>"
        print "\n-------------需要在目标库上创建的表------------"
        self.create_sql(self.mysql_b, lacks)
        print "------------------THE END---------------------\n"

        print "\n-------------提醒：原始库上缺少的表------------"
        self.create_sql(self.mysql_a, more)
        print "------------------THE END---------------------\n"

        print "\n************************************比对属性列表(-为缺少；+为多余；<>为不同)****************************************"
        names = ["NAME", "TYPE", "IS_NULL", "IS_PRIMARY", "DEFAULT_VALUE", "IS_INCREMENT"]
        for table in common:
            fields_a = {}
            for row in  self.mysql_a.query("DESC `%s`" % (table)):
                fields_a[row[0]] = row

            fields_b = {}
            for row in  self.mysql_b.query("DESC `%s`" % (table)):
                fields_b[row[0]] = row

            m, c, l = self.diff(fields_a.keys(), fields_b.keys())
            for name in m:
                print "    +", table, ":", fields_a[name]
            for name in l:
                print "    -", table, ":", fields_b[name]
            for name in c:
                if not self.same(fields_a[name], fields_b[name]):
                    print "    <>", table, ":", fields_a[name], fields_b[name]
        else:
            print "无"
        print "------------------THE END--------------------\n"

    def run_data(self, data):
        tables_a = [row[0] for row in self.mysql_a.query("SHOW TABLES")]
        tables_b = [row[0] for row in self.mysql_b.query("SHOW TABLES")]
        more, common, lacks = self.diff(tables_a, tables_b)
        for table in common:
            if re.match(enum_re, table):
                sql = "select * from %s"%table
                name_sql = "select COLUMN_NAME from information_schema.COLUMNS where table_name = '%s'"%table
                table_a = self.mysql_a.query(sql)
                table_b = self.mysql_b.query(sql)
                tab_a_name = self.mysql_a.query(name_sql)
                tab_b_name = self.mysql_b.query(name_sql)
                # 对比数据缺失
                more, common, lacks = self.diff(table_a, table_b)
                tab_a = list(set(table_a).difference(set(table_b)))
                tab_b = list(set(table_b).difference(set(table_a)))
                if len(tab_a) + len(tab_b) != 0:
                    lack_a = []
                    lack_b = []
                    # 不同之处
                    diff_a = []
                    diff_b = []
                    for i in range(len(tab_a)):    
                        lack_a.append(tab_a[i][0])
                    for i in range(len(tab_b)):
                        lack_b.append(tab_b[i][0])
                    tab = list(set(lack_a).intersection(set(lack_b)))
                    for i in range(len(tab_a)):
                        if tab_a[i][0] in tab:
                            diff_a.append(tab_a[i])
                    for i in range(len(tab_b)):
                        if tab_b[i][0] in tab:
                            diff_b.append(tab_b[i])
                    for i in diff_a:
                        tab_a.remove(i)
                    for i in diff_b:
                        tab_b.remove(i)
                    print "<h1>表格:{}</h1>".format(table)
                    if tab_a_name != tab_b_name:
                        print "<h3>字段不同</h3>\n"
                        print "目标库:{}".format(sys_utf8.Utf8(tab_a_name))
                        print "源库：{}".format(sys_utf8.Utf8(tab_b_name))

                        print "备注： 字段不同不能累加数据，请选择需要覆盖的库,(同步表的结构并且覆盖数据)"
                    if len(tab_a) + len(tab_b) != 0:
                        print "<h3>数据缺失部分:</h3>\n"
                        print ">>>>目标库存在的数据<<<<:"
                        if len(tab_a) == 0:
                            print "无数据"
                        else:
                            for tab in tab_a:
                                tab =  db_util.ParseUtime(tab)
                                tab_a = sys_utf8.Utf8(tab)
                                print "{}\n".format(tab_a)
                        print 
                        print ">>>>源库存在的数据：<<<<:"
                        if len(tab_b) == 0:
                            print "无数据"
                        else:
                            for tab in tab_b:
                                tab = db_util.ParseUtime(tab)
                                tab_b = sys_utf8.Utf8(tab)
                                print "{}\n".format(tab_b)
                    if  len(diff_a) + len(diff_b) != 0:
                        print "<h3>不同之处:</h3>"
                        for i in diff_a:
                            diff_data = []
                            for x in diff_b:
                                if x[0] == i[0]:
                                    i = db_util.ParseUtime(i)
                                    x = db_util.ParseUtime(x)
                                    i = sys_utf8.Utf8(i)
                                    x = sys_utf8.Utf8(x)
                                    print "目标:{}".format(i)
                                    print "源库:{}\n".format(x)

                    result1 = """
                         <li>将目标库数据同步到源库<a href="/sync_manna_ol_dev?target=0&table={}&data={}">(覆盖)</a>&nbsp<a href="/sync_manna_ol_dev?target=2&table={}&data={}">(累加)</a></li>
                        """.format(table, data, table, data)
                    result2 = """
                        <li>将源库数据同步到目标库<a href="/sync_manna_ol_dev?target=1&table={}&data={}">(覆盖)</a>&nbsp<a href="/sync_manna_ol_dev?target=3&table={}&data={}">(累加)</a></li>                                  
                        """.format(table, data, table, data)
                    print result1,result2

    def run_data_sync(self, table, target):
        sql = "select * from %s"%table
        del_sql = "truncate table %s"%table
        sql_name = "select COLUMN_NAME from information_schema.COLUMNS where table_name = '%s'"%table

        if target == "0": # 将目标库数据同步到源库
            self.mysql_query(self.mysql_a, self.mysql_b,  sql, del_sql, table, target)
        if target == "1": # 将源库的数据同步到目标库
            self.mysql_query(self.mysql_b, self.mysql_a,  sql, del_sql, table, target)
        if target == "2": #将目标库的数据追加到源库 
            self.mysql_query(self.mysql_a, self.mysql_b,  sql, del_sql, table, target)
        if target == "3": # 将源库数据追加目标库
            self.mysql_query(self.mysql_b, self.mysql_a,  sql, del_sql, table, target)
        return 1


    def mysql_query(self,mysql1, mysql2, sql, del_sql, table, tarage):
        sql_name = "select COLUMN_NAME from information_schema.COLUMNS where table_name = '%s'"%table
        clear_sql = "drop table %s"%table
        desc_sql = "show create table %s "%table

        # 字段是否相等
        table_1_name = mysql1.query(sql_name)
        table_2_name = mysql2.query(sql_name)
        table_b = mysql1.query(sql)
        if tarage in ["0", "1"]:
            if table_1_name != table_2_name:
                table_1_desc = mysql1.query(desc_sql)
                mysql2.query(clear_sql)
                mysql2.query(table_1_desc[0][1])
            mysql2.query(del_sql)
        list1 = list()
        for name in table_1_name:
            name = "".join(name)
            list1.append(str(name))
            for table_ in table_b:
                values = list()
                for v in table_:
                    if v is None or v ==" ":
                        v = ""
                    if isinstance(v,int) or isinstance(v,long):
                        values.append(str(v))
                    elif isinstance(v, str) or isinstance(v, unicode):
                        values.append("'"+v+"'")
                    elif isinstance(v, datetime.datetime): 
                        values.append("'"+db_util.ParseUtime(v)+"'")
                    elif isinstance(v,float):
                        values.append(str(v))
                print values
                insert = "insert into {} ({}) values ({})".format(table, ",".join(list1), ",".join(values))
                rowcount, primaryid = mysql2.execute(insert)

        
"""
if __name__ == '__main__':
    import pyutil.db.tool.db_compare.settings as settings
    s = Shower(settings.config_A, settings.config_B, settings.ignores) 
    s.run_data_sync(enum_analog_type,0)
"""
