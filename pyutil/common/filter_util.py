#!/usr/bin/python
#-*- coding:utf-8 -*-

import pyutil.common.sys_utf8 as sys_utf8

def sift(data_list, filter_list):
    def sift_by_filter(data_list, filter_func):
        result = []
        for data in data_list:
            if filter_func(data):
                 result.append(data)
        return result

    for filter_func in filter_list:
        data_list = sift_by_filter(data_list, filter_func)
    return data_list


def test():
    data_list = [{"id":1}, {"id":2}, {"id":4}, {"id":7},]
    print sift(data_list, [lambda x: x["id"] > 3])


if __name__ == '__main__':
    test()
