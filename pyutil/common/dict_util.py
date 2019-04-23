#!/usr/bin/python
#-*- coding:utf-8 -*-

import pyutil.common.sys_utf8 as sys_utf8


def Contain(dic_container, dic_some):
    for k in dic_some or {}:
        if k not in dic_container or dic_some[k] != dic_container.get(k):
            return False
    return True

class BaseDict(dict):
    '''
    通过使用__setattr__,__getattr__,__delattr__
    可以重写dict,使之通过“.”调用
    '''

    def __init__(self, *args):
        for arg in args:
            if not isinstance(arg, dict):
                self[str(arg)] = ''
            else:
                self.update(arg)

    def __setattr__(self, key, value):
        self[key] = value
        
    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError as k:
            return None
            
    def __delattr__(self, key):
        try:
            del self[key]
        except KeyError as k:
            return None
            
    def __call__(self, key=None):
        try:
            return self[key] if key else self
        except KeyError as k:
            return "In '__call__' error"


def DictFilter(someMap, someFields):
    curDict = BaseDict()
    for k in someFields:
        if k in someMap:
            curDict[k] = someMap[k]
    return curDict


def List2Dict(records, jsonpath):
    if isinstance(jsonpath, str) or isinstance(jsonpath, unicode):
        jpath = jsonpath.split(".")
    else:
        jpath = jsonpath

    def get_jval(r, jpath):
        v = r
        for j in jpath:
            v = v.get(j)
        return v

    result = {}
    for r in records:
        k = get_jval(r, jpath)
        result.setdefault(k, []).append(r)
    return result


def Dict2Values(results):
    records = []
    for k in results:
        vals = results[k]
        if isinstance(vals, list) or isinstance(vals, tuple):
            records.extend(vals)
        elif isinstance(vals, dict):
            records.append(vals)
    return records


def FilterSpaceElement(dict_obj):
    for key in list(dict_obj.keys()):
        value = dict_obj[key]
        if (isinstance(value, str) or isinstance(value, unicode)) and value.strip() == "":
            del dict_obj[key]
        if value == {}:
            del dict_obj[key]
        if isinstance(value, dict):
            value = FilterSpaceElement(value)
            if value == {}:
                del dict_obj[key]
    return dict_obj


def test():
    s = BaseDict("a","b")
    s["c"]="999"
    s.a = 333
    print(s())
    
    s.name = "drogher"
    s.age = 28

    s.tmp = "abc"
    print(s())

    del s.tmp
    print(s())

def test2():
    a = DictFilter({"a":1, "b":2, "c":3}, ["a", "c", "d"])
    print a


if __name__ == '__main__':
    # test2()
    d = {
        "info_company":{
            "company_name":"asd",
            "company_address":"四川省自贡市大安区马冲口街道",
            "company_region":"",
            "enum_company_type":{
                "id":"0"
            },
            "contact_phone":"",
            "setup_time":"",
            "post_code":"",
            "staff_total":"",
            "enum_company_regulator_level":{
                "id":""
            },
            "legal_representative_name":"",
            "legal_representative_code":"",
            "legal_representative_phone":"",
            "permanent_assets":"",
            "enum_company_economic":{
                "id":""
            },
            "company_code":"",
            "thing_type":"info_company_cared"
        },
        "info_company_cared":{
            "site_area":"",
            "building_area":"",
            "company_graph":"",
            "center_name":"",
            "authority_company_name":"",
            "dominate_company_name":"",
            "control_room_phone":"",
            "safety_responsibility_name":"",
            "safety_responsibility_phone":"",
            "safety_manager_code":"",
            "safety_manager_name":"",
            "safety_manager_phone":"",
            "safety_responsibility_code":"",
            "parttime_responsibility_name":"",
            "parttime_responsibility_phone":"",
            "parttime_responsibility_code":"",
            "company_name":"asd"
        },
        "info_user":{
            "enum_user_type":{
                "id":"2"
            },
            "enum_user_role":{
                "id":"9"
            },
            "company_id":"",
            "company_type":"info_company_cared",
            "account":"15201512146",
            "password":"15201512146",
            "name":"15201512146",
            "phone_num":"15201512146"
        },
        "info_location":{
            "address":"四川省自贡市大安区马冲口街道",
            "longitude":104.773482,
            "latitude":29.376626
        }
    }
    FilterSpaceElement(d)
    print d