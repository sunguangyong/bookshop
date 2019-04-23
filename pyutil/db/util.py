# -*- coding: utf-8 -*- 

import datetime
import functools
import time

def func_cache(func):

    cache = {}
    last = {}

    @functools.wraps(func)
    def _inner(*args):
        key = func.__name__+"@"+args[1]
        if key not in cache or last.get(key, 0)+120<time.time():
            last[key] = time.time()
            cache[key] = func(*args)
        return cache[key]
    return _inner

def ParseUtime(data):
    if isinstance(data, list) or isinstance(data, tuple):
        result = []
        for item in data:
            result.append(ParseUtime(item))
        return result
    elif isinstance(data, dict):
        result = {}
        for key in data:
			result[key]=ParseUtime(data[key])
        return result
    elif isinstance(data, datetime.datetime):
        try:
            return data.strftime('%Y-%m-%d %H:%M:%S')
        except Exception, e:
            return "0000-00-00 00:00:00"
    elif isinstance(data, datetime.date):
        try:
            return data.strftime('%Y-%m-%d')
        except Exception, e:
            return "0000-00-00"
    else:
        return data


if __name__ == '__main__':
    a= [{'a':123},{'b':'c'}]
    print ParseUtime(a)
    b =  [(103, u'12210', u'12210', u'12210', u'12210', 1, datetime.datetime(2017, 12, 6, 20, 22, 8))]
    print ParseUtime(b)
