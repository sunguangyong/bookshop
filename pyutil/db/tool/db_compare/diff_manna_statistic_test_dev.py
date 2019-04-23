# -*- coding: utf-8 -*-

import pyutil.common.sys_utf8

if __name__ == '__main__':
    import pyutil.db.tool.db_compare.manna_statistic_test_dev_settings as settings
    import pyutil.db.tool.db_compare.shower as shower

    print "目标库:manna_statistic_test"
    print "源库:manna_statistic_dev"
    s = shower.Shower(settings.config_A, settings.config_B, settings.ignores)
    s.run()
