# -*- coding: utf-8 -*-

import pyutil.common.sys_utf8
import pyutil.db.tool.db_compare.shower as shower

if __name__ == '__main__':

    print "目标库:测试环境的realtime_shenyang"
    print "源库:线上的realtime_shenyang"

    import pyutil.db.tool.db_compare.test_shenyang_settings as settings
    s = shower.Shower(settings.config_A, settings.config_B, settings.ignores) 
    s.run()
