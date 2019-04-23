# -*- coding: utf-8 -*- 

import pyutil.common.sys_utf8 as sys_utf8
import pyutil.db.mellow as mellow
import pyconf.db.manna as manna

mysql = mellow.mellow(manna.config)

def get_system_id(thing_id):
    rows = mysql.Find("relation_things_system", "system_id", {"thing_id": thing_id})
    return rows[0][0] if rows else -1
