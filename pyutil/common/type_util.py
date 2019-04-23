#!/usr/local/bin/python
# -*- coding: utf8 -*-

def is_str(s):
    return isinstance(s, unicode) or isinstance(s, str)

def is_int(i):
    return isinstance(i, long) or isinstance(i, int)

def is_array(a):
    return isinstance(a, tuple) or isinstance(a, list)

def is_dict(d):
    return isinstance(d, dict)
