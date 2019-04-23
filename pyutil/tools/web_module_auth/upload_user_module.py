# -*- coding: utf-8 -*- 

import pyutil.common.sys_utf8 as utf8
import os
import json
import sys

import pyutil.db.mellow as mellow
import pyconf.db.manna_apps as manna_apps

mysql = mellow.mellow(manna_apps.config)


combo_id = 0


def upload_user_module(uid, combo_id):
    auth_map = {}
    rows = mysql.Find("info_web_combo_module", [], {"combo_id": combo_id}, out=dict)
    for row in rows:
        record = {}
        record["user_id"] = uid
        record["module_id"] = row["module_id"]
        record["auth"] = row["auth"]
        print record
        mysql.UpOrInsert("info_web_user_module", record, {"user_id": record["user_id"], "module_id": record["module_id"]})


if __name__ == '__main__':
    if len(sys.argv)<3:
        print "Usage:\n     python -m upload_combo_module 101"
        sys.exit(-1)
    uid = sys.argv[1] 
    combo_id = sys.argv[2] 
    result = upload_user_module(uid, combo_id)
    print result
