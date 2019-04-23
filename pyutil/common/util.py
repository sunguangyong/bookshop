#!/usr/bin/python
#-*- coding:utf-8 -*-
import re
import time

import sys
import json
import struct
import pyutil.common.type_util as type_util


def uchar_checksum(data, byteorder='little'):
        length = len(data)
        checksum = 0
        for i in range(0, length):
                checksum += struct.unpack("<B",data[i:i+1])[0]
                checksum &= 0xFF
        return struct.pack("B", checksum)


def FilterMap(dataMap, keys):
    if isinstance(dataMap, dict):
        return dict(filter(lambda x: x[0] in keys and x[1]!=None, dataMap.items()))
    if isinstance(dataMap, list):
        return [dict(filter(lambda x: x[0] in keys and x[1]!=None, d.items())) for d in dataMap]


def PrintCn(item):
    return json.dumps(item) 


def get_imei(data):
    result = 0
    datas = data[::-1]
    for i in datas:
        result = (result << 8) + int(i, 16)
    return result


def check_mac(addr):
    """Validates a mac address"""
    valid = re.compile(r'''
                      (^([0-9A-F]{1,2}[-]){5}([0-9A-F]{1,2})$
                      |^([0-9A-F]{1,2}[:]){5}([0-9A-F]{1,2})$
                      |^([0-9A-F]{1,2}[.]){5}([0-9A-F]{1,2})$)
                      ''',
                       re.VERBOSE | re.IGNORECASE)
    return valid.match(addr) is not None