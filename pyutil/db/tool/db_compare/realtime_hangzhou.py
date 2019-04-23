# -*- coding: utf-8 -*-

import pyutil.common.sys_utf8

if __name__ == '__main__':
    import pyutil.db.tool.db_compare.hangzhou_settings as settings
    import pyutil.db.tool.db_compare.shower as shower

    print "目标库:realtime_hangzhou"
    print "源库:realtime_db"
    s = shower.Shower(settings.config_A, settings.config_B, settings.ignores) 
    s.run()
