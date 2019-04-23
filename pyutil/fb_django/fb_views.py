#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import re
import sys
import pyutil.common.sys_utf8 as Utf8Lib
import pyutil.common.type_util as type_util

from pyutil.common.dict_util import BaseDict
from pyutil.fb_django.fb_mixin import RequestMixin, LoginMixin, PermissionMixin
from pyutil.fb_django.fb_error import ResponseCode
from rest_framework.views import APIView
from django.http import HttpResponse



class BaseView(RequestMixin):

    def __init__(self):
        self.page_no = 0
        self.page_size = 50
    
    def check_query(self, fields=[]):
        """检查字段是否正确"""
        def _check_data_type(v, typename):
            try:
                if typename == "int":
                    int(v)
                elif typename == "float":
                    float(v)
                elif typename == "str":
                    str(v)
                return True
            except ValueError:
                return False


        for field in fields:
            _field = field
            _type = "str"
            
            arr = field.split(':')
            if len(arr) < 2:
                _field = arr[0]
            else:
                _field = arr[1]
                _type = arr[0]
            if _field not in self.url_params.keys():
                return "POST_FORMAT_ERR",  "LACK PARAMS_REQUIRED: " + _field
            elif not _check_data_type(self.url_params.get(_field), _type):
                return "POST_FORMAT_ERR",  "PARAM [%s] DATA TYPE ERROR : %s" % (_field, _type)
        return None



    #检查post数据的完整性
    def check_post(self, post_frame={}):
        for name, value in post_frame.items():
            data = self.post_body.get(name)
            if not data:   #level 1
                return "POST_FORMAT_ERR",  "LACK POST FIELD:" + name
            if type_util.is_dict(value):
                if not type_util.is_dict(data):
                    return "POST_FORMAT_ERR",  "Error POST FIELD Type (%s) MUST BE  A DICT" % (name)

                for key, val in value.items():
                    data_val = data.get(key)
                    if data_val is None: #level 2
                        return "POST_FORMAT_ERR",  "LACK POST FIELD:%s.%s" % (name, key)
                    if type_util.is_dict(val):
                        if not type_util.is_dict(data_val):
                            return "POST_FORMAT_ERR",  "Error POST FIELD Type (%s.%s) MUST BE  A DICT" % (name, key)

                        for k, v in val.items():
                            data_v = data_val.get(k)
                            if data_v is None:  #level 3
                                return "POST_FORMAT_ERR",  "LACK POST FIELD:%s.%s.%s" % (name, key, k)
        return None

    # 响应成功
    def send_success(self, data=None):
        return self.__response("SUCCESS", data, None)
    
    # 响应错误
    def send_error(self, code=None, argv=None):
        if code is None or len(code) < 1:
            code = 'UNKNOW'
        return self.__response(code, None, argv)

    # 透传错误信息
    def send_api_error(self, data=None):
        return HttpResponse(Utf8Lib.Utf8(data), status=200, content_type="application/json")

    # 响应数据
    def send(self, code, data, argv):
        return self.__response(code, data, argv)

    def send_response(self, result):
        return HttpResponse(Utf8Lib.Utf8(result), status=200, content_type="application/json")


    # 响应文件流
    def send_file(self, response, headers={}):
        for key in headers:
            response[key] = headers[key]
        return response


    def __response(self, code, data, argv):
        jsn = ResponseCode.build(code, data, argv)
        return HttpResponse(Utf8Lib.Utf8(jsn), status=200, content_type="application/json")

    #把分页器转为切片器
    def parse_limit(self):
        page_no = int(self.url_params.get("page_no") or 0)
        if page_no <0:
            page_no = 0

        page_size = int(self.url_params.get("page_size") or sys.maxint)
        if page_size <0 or page_size >100:
            page_size = 100
        
        start = page_no * page_size
        end = (page_no+1) * page_size
        limit = (start, end)

        return limit


class GeneralView(BaseView, LoginMixin, PermissionMixin, APIView, BaseDict):
    pass



class NoLoginView(BaseView, APIView, BaseDict):
    pass

