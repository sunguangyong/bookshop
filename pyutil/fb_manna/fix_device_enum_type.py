# -*- coding: utf-8 -*- 

import pyutil.common.sys_utf8 as sys_utf8
import pyutil.db.mellow as mellow
import pyconf.db.manna as manna

mysql = mellow.mellow(manna.config)

def fix_device_type():
    type_map = {}
    for row in mysql.Find("enum_device_model", [], out=dict):
        type_map[row["id"]] = row

    for row in mysql.Find("info_device", [], out=dict):
        enum_device_model = row["enum_device_model"]
        enum_device_type = type_map[enum_device_model]["enum_device_type"] if type_map.get(enum_device_model) else -1
        enum_device_class = type_map[enum_device_model]["enum_device_class"] if type_map.get(enum_device_model) else -1

        print "info_devcie", {"enum_device_type":enum_device_type, "enum_device_class":enum_device_class}, {"thing_id":row["thing_id"]}
        mysql.Update("info_device", dataMap={"enum_device_type":enum_device_type, "enum_device_class":enum_device_class}, indexMap={"thing_id":row["thing_id"]})



if __name__ == "__main__":
    fix_device_type()
