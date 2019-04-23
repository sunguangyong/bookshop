# -*- coding: utf-8 -*-

import json
import type_util
import copy

def get_value(path, record):
    def _value(temp, _j):
        return temp.get(_j)
    if path and record and type_util.is_dict(record):
        _temp = record
        paths = path.split(".")
        for j in paths:
            if not _temp:
                break
            _temp = _value(_temp, j)

        return _temp
    return None
        


