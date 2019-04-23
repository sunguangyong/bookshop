# -*- coding: utf-8 -*- 

import pyutil.common.sys_utf8 as utf8
import os
import json
import sys

import pyutil.db.mellow as mellow
import pyconf.db.manna_apps as manna_apps
import pyutil.common.datetime_util as datetime_util

mysql = mellow.mellow(manna_apps.config)


def get_user_auth(uid):
    if not uid:
        print "Error, uid is None"
        return {}
    rows = mysql.Find("relation_user_template", ["template_id", "buy_id"], {"user_id":uid})
    if not rows:
        print "Error, user's combo not found, uid=", uid
        return {}

    template_id = rows[0][0]
    buy_id = rows[0][1]
    print "template_id:::", uid, template_id 
    if check_buy_platform_status(buy_id):
        return get_template(template_id)
    else:
        return []


def check_buy_platform_status(buy_id):
    """检查购买的平台是否可用"""
    if buy_id == -1:
        return True
    rows = mysql.Find("info_web_buy_platform", ["status","platform_end_time"], {"buy_id": buy_id})
    if not rows:
        return False

    if rows[0][0] < 1:
        return False

    if rows[0][1] < datetime_util.TimeNow():
        return False

    return True


def data2json(rows, enum_user_type):
    if not rows:
        return []
    auth_map = {}
    for row in rows:
        auth_map[row["module_id"]] = row["auth"]
    module_map = {}
    rows = mysql.Find("info_web_module", [], {"enum_user_type" : enum_user_type}, out=dict)
    for row in rows:
        row["is_active"] = row["auth"]
        row["auth"] = int(auth_map[row["module_id"]])
        row["children"] = []

        row["id"] = row["module_id"]
        row["pid"] = row["module_pid"]
        row["children"] = []
        del row["module_id"]
        del row["module_pid"]
        del row["create_time"]
        del row["update_time"]
        del row["creater_id"]
        module_map[row["id"]] = row

    result = []
    for row in rows:
        pid = row["pid"]
        if not pid:
            result.append(row)
        else:
            module_map[pid]["children"].append(row)
    return result


def get_template_by_user_role(platform_id, enum_user_type, enum_user_role):
    rows = mysql.Find("info_web_platform_template", ["template_id"], {"platform_id":platform_id, "enum_user_type" : enum_user_type, "enum_user_role" : enum_user_role}, out=dict)
    template_id = rows[0]["template_id"]
    return get_template(template_id, enum_user_type)


def get_template(template_id, enum_user_type=None):
    if not enum_user_type:
        rows = mysql.Find("info_web_platform_template", ["enum_user_type"], {"template_id": template_id}, out=dict)
        enum_user_type = rows[0]["enum_user_type"]
    rows = mysql.Find("info_web_template_module", [], {"template_id": template_id}, out=dict)
    return data2json(rows, enum_user_type)

def test():
    if len(sys.argv)<3:
        print "Usage:\n     python -m get_user_combo 1 101"
        sys.exit(-1)
    uid = sys.argv[1] 
    combo_id = sys.argv[2] 
    result = get_user_combo(uid, combo_id)
    print result

def test1():
    uid = sys.argv[1] 
    result = get_user_auth(uid)
    print result

if __name__ == '__main__':
    # test1()
    get_template(1010108)

