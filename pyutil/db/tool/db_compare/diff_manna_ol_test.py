# -*- coding: utf-8 -*-

import pyutil.common.sys_utf8

if __name__ == '__main__':
    import pyutil.db.tool.db_compare.manna_ol_test_settings as settings
    import pyutil.db.tool.db_compare.shower as shower

    print "目标库:manna_ol"
    print "源库:manna_test"
    s = shower.Shower(settings.config_A, settings.config_B, settings.ignores)
    s.run()
