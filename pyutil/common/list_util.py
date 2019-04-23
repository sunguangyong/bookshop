# -*- coding: utf-8 -*-

import pyutil.common.type_util as type_util

def diff(list_a, list_b, ignores=[]):
    more = [a for a in [a for a in list_a if a not in list_b ] if a not in ignores ]
    common = [c for c in [c for c in list_a if c in list_b ] if c not in ignores ]
    lacks = [b for b in [b for b in list_b if b not in list_a] if b not in ignores ]
    return more, common, lacks

def contain(list_a, list_b):
    if not type_util.is_array(list_a) or not type_util.is_array(list_b):
        return False

    for a in list_a:
        if a not in list_b:
            return False
    return True

def union(list_a, list_b):
    return list(set(list_a).union(set(list_b)))

def test():
    list_a=[1,2,3,4,5]
    list_b=[4,5,6,7,8]
    print union(list_a, list_b)


if __name__ == '__main__':
    test()