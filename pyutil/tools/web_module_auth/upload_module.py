# -*- coding: utf-8 -*- 

import pyutil.common.sys_utf8 as utf8
import os
import sys 
import json

import pyutil.db.mellow as mellow
import pyconf.db.manna_apps as manna_apps

mysql = mellow.mellow(manna_apps.config)


def parse(pid, modules):
    records = []
    for module in modules:
        record = {}
        record["module_id"] = module["id"]
        record.update({k: module[k] for k in module if k in [ "name", "route", "type", "desc"]})
        record["module_pid"] = pid
        record["auth"] = module["authorization"] 
        records.append( record )
        if module.get("children"):
            records.extend( parse(module["id"], module["children"]) )
    return records
        
        


if __name__ == '__main__':
    
    if len(sys.argv)<2:
        print "Usage:\n     python -m pyutil/tools/web_module_auth/upload_module 1"
        sys.exit(-1)

    global type_id 
    type_id =  int(sys.argv[1])
    
    f = open("./pyutil/tools/web_module_auth/auth_%d.json" % (type_id))
    modules = json.loads(f.read())
    
    records = parse("", modules)
    for record in records:
        record.update({"enum_user_type":type_id})
        print "|||", record
        mysql.UpOrInsert("info_web_module", record, {"module_id": record.get("module_id"), "enum_user_type" : type_id})
