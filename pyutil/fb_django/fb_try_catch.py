#!/usr/bin/env python
# -*- coding: utf-8 -*-

import functools
import pyutil.common.sys_utf8 as sys_utf8
from pyutil.fb_django.fb_views import GeneralView
import traceback

def try_catch():
    def _decorater(func):
        @functools.wraps(func)
        def _wrapped_func(general_view, *args, **kwargs):
            try:
                return func(general_view, *args, **kwargs)
            except Exception,e:
                print '\n###########################################'
                print 'str(Exception):\t', str(Exception)
                print 'str(e):\t\t', str(e)
                print 'repr(e):\t', repr(e)
                print 'e.message:\t', e.message
                print 'traceback.print_exc():'; traceback.print_exc()
                print 'traceback.format_exc():\n%s' % traceback.format_exc()
                print '###########################################\n'
                return general_view.send_error("EXCEPTION", str(e))
        return _wrapped_func
    return _decorater
