# -*- coding: utf-8 -*-
#__author__ = 'basearch'

import os
import sys
import xlrd
import pyutil.common.sys_utf8 as sys_utf8
import pyconf.db.manna as manna
import pyutil.db.mellow as mellow

eng_name_map = {
    "enum_company_online_status" : "eng_status",
    "enum_device_online_status" : "eng_status",
    "enum_user_status" : "eng_status",
}

mysql = mellow.mellow(manna.config)

def parse():
    for root, dirs, files in os.walk("pyutil/tools/import_manna_eng/manna_eng/", topdown=False):
        for f_name in files:
            table_name = f_name[:f_name.find(".")]
            print table_name
            field_name = eng_name_map.get(table_name, "eng_name")

            data = xlrd.open_workbook('pyutil/tools/import_manna_eng/manna_eng/%s.xls' % (table_name))
            table = data.sheets()[0] 
            
            for i in range(0, table.nrows):
                print i
                record = table.row_values(i)
                id, eng_val = record[0], record[-1]
                print table_name, {field_name: eng_val}, {"id":id}
                mysql.Update(table_name, {field_name: eng_val}, {"id":int(id)})
                print record

    


if __name__ == '__main__':
    parse()
