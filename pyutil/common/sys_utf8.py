#!/usr/local/bin/python
# -*- coding: utf8 -*-

import json
import time
import datetime

import sys
reload(sys)
sys.setdefaultencoding('utf8')

import pyutil.common.type_util as type_util


def __info():
     try:
         raise Exception
     except:
         f = sys.exc_info()[2].tb_frame.f_back
     return '%s %s %s %d | ' % (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())), f.f_code.co_filename, f.f_code.co_name, f.f_lineno)


def Utf8(s):
    if not s:
        return str(s)
    if type_util.is_dict(s) or type_util.is_array(s):
        encoder = json.JSONEncoder(encoding = 'utf-8', ensure_ascii = False)  #其他编码的不会被转成unicode
        return encoder.encode(s)
    elif type_util.is_str(s):
        return s.encode("utf-8")
    else:
        return str(s)


def Print(s):
    print Utf8(s)

def test():
    print __info(), "abc"

if __name__ == '__main__':
    obj = {"name":"好的", "jsn":"{\"age\":1}"}
    Print(obj)
    test()
