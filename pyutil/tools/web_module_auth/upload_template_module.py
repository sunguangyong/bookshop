# -*- coding: utf-8 -*- 

import pyutil.common.sys_utf8 as utf8
import os
import json
import sys

import pyutil.db.mellow as mellow
import pyconf.db.manna_apps as manna_apps

mysql = mellow.mellow(manna_apps.config)



def parse(data):
    records = []
    for module in data:
        record = {}
        record["module_id"] = module.get("id", "")
        if not record["module_id"]:
            continue
        record["auth"] = module.get("authorization")
        records.append(record)
        if module.get("children"):
            records.extend(parse(module["children"]))
    return records


def set_template_module(data, template_id):
    records = parse(data)
    mysql.Delete("info_web_template_module", {"template_id":template_id})
    fields = ["template_id", "module_id", "auth"]
    values = []
    for record in records:
        values.append((template_id, record["module_id"], record["auth"]))
    mysql.InsertMany("info_web_template_module", fields, values)


if __name__ == '__main__':
    if len(sys.argv)<2:
        print "Usage:\n     python -m upload_combo_module 101"
        sys.exit(-1)

    template_id =  int(sys.argv[1])

    f = open("./pyutil/tools/web_module_auth/data/%d.json" % (template_id))
    data = json.loads(f.read())
    set_template_module(data, template_id)
