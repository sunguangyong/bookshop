# -*- coding: utf-8 -*- 

import pyutil.common.sys_utf8
import pyutil.db.mellow as mellow
import pyconf.db.realtime_shenyang as realtime_shenyang
import pyconf.db.realtime_db as realtime_db
import time
import sys


start = time.time()
mysql_w = mellow.mellow(realtime_db.config_w)
if len(sys.argv)==2 and sys.argv[1] == "shenyang":
    mysql_w = mellow.mellow(realtime_shenyang.config_w)
print "cost:", time.time() - start
