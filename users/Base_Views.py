#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import re
import sys
import pyutil.common.sys_utf8 as Utf8Lib
import pyutil.common.type_util as type_util

from rest_framework.views import APIView
from django.http import HttpResponse

import copy


class ResponseCode:
    CODE_DICT = {
        # 常用验证提示
        "SUCCESS": {"code": 0, "msg": u"操作成功", "eng_msg": "successful"},
        "EXCEPTION": {"code": 9999, "msg": u"异常错误 : {0}", "eng_msg": "exception error : {0}"},
        "UNKNOW": {"code": 9998, "msg": u"未知错误", "eng_msg": "unknow error"},
        "ILLEGAL": {"code": 9997, "msg": u"非法请求", "eng_msg": "illegal error"},
        "TOKEN_ERR": {"code": 9996, "msg": u"Token不正确或者已经过期", "eng_msg": "token has expired"},
        "QUERY_NO_DATA": {"code": 9995, "msg": u"查询无任何数据 : {0}", "eng_msg": "no data"},
        "ATOM_ERR": {"code": 9994, "msg": u"原子封装信息错误", "eng_msg": "atom error"},
        "AUTH_ERR": {"code": 9993, "msg": u"无访问权限", "eng_msg": "no access right"},

        # 请求参数提示
        "PARAMS_TYPE_ERR": {"code": 8999, "msg": u"参数类型有误 : {0}", "eng_msg": "param error"},
        "PARAMS_REQUIRED": {"code": 8998, "msg": u"缺少必要的参数 : {0}", "eng_msg": "param error"},
        "PARAMS_FORMAT_ERR": {"code": 8997, "msg": u"参数格式不正确 : {0}", "eng_msg": "param foramt error : {0}"},
        "POST_FORMAT_ERR": {"code": 8996, "msg": u"POST数据格式不正确 : {0}", "eng_msg": "post data error : {0}"},

        # 新增数据失败
        "ADD_DATA_ERR": {"code": 7999, "msg": u"添加数据失败 : {0}", "eng_msg": "add failed : {0}"},
        "UPDATE_DATA_ERR": {"code": 7998, "msg": u"修改数据失败 : {0}", "eng_msg": "modify failed : {0}"},
        "DELETE_DATA_ERR": {"code": 7997, "msg": u"删除数据失败 : {0}", "eng_msg": "delete failed : {0}"},
        "UNIQUE_DATA_ERR": {"code": 7996, "msg": u"参数唯一性校验失败 : {0}", "eng_msg": "param unique error: {0}"},
        "EXIST_DATA_ERR": {"code": 7995, "msg": u"数据已存在: {0}", "eng_msg": "data exist: {0}"},
        "CHECK_DATA_ERR": {"code": 7994, "msg": u"数据校验失败: {0}", "eng_msg": "check data failed: {0}"},
        "RECORD_CAN_NOT_DELELE": {"code": 7993, "msg": u"平台不能被删除: {0}", "eng_msg": "record cant be deleted: {0}"},
        "TEMPLATE_CAN_NOT_DELELE": {"code": 7992, "msg": u"模板不能被删除: {0}", "eng_msg": "record cant be deleted: {0}"},

        # 应用中心市场
        "HAS_BAN_WORDS": {"code": 10000, "msg": u"内容中含有违规文字 : {0}", "eng_msg": "baned words: {0}"},
        "NO_RECOMMENT": {"code": 10001, "msg": u"不能重复评论", "eng_msg": "no recomment"},
        "NO_ADD_APP": {"code": 10002, "msg": u"{0}无法添加该应用", "eng_msg": "the app cannot be added"},
        # 主管用户不能添加系统应用

        # 用户以及登录相关
        "LOGIN_FAILED": {"code": 6999, "msg": u"登录失败", "eng_msg": "login failed"},
        "ACCOUNT_BAN": {"code": 6998, "msg": u"账号已被禁用", "eng_msg": "account has been banned"},
        "UPDATE_PWD_ERR": {"code": 6997, "msg": u"修改密码失败", "eng_msg": "failed to change password"},
        "UPDATE_USER_ERR": {"code": 6996, "msg": u"用户不能被停用", "eng_msg": "Users cannot be stopped"},
        "DELETE_USER_ERR": {"code": 6995, "msg": u"用户不能被删除", "eng_msg": "Users cannot be delete"},
        "PASSWORD_ERROR": {"code": 6994, "msg": u"密码错误", "eng_msg": "password error"},
        "USER_NOT_EXISTS": {"code": 6993, "msg": u"用户不存在", "eng_msg": "user not exists"},

        # 摄像头
        "SETTING_PERMISSION_FAILED": {"code": 6992, "msg": u"设置权限失败", "eng_msg": "Setting permission failed"},
        "OPEN_LIVE_FAILED": {"code": 6991, "msg": u"开通直播失败", "eng_msg": "open live failed"},
        "GET_LIVE_ADDRESS_FAILED": {"code": 6990, "msg": u"获取直播地址失败", "eng_msg": "get live failed"},
        "CREATE_RAM_ACCOUNT": {"code": 6989, "msg": u"子账号失效", "eng_msg": "create ram account"},
        "ADD_TO_FAILED": {"code": 6988, "msg": u"添加摄像头失败", "eng_msg": "add to failed"},

    }

    @classmethod
    def build(cls, key, data=None, agrv=None):
        if cls.CODE_DICT.has_key(key):
            jsn = copy.deepcopy(cls.CODE_DICT[key])
            if agrv:
                jsn["msg"] = jsn["msg"].format(agrv)
                jsn["eng_msg"] = jsn["eng_msg"].format(agrv)

            if data is not None:
                jsn["data"] = data
            return jsn
        else:
            raise RuntimeError("key:" + key + u" 不存在与ResponseCode字典中")

    @classmethod
    def build_success(cls, data):
        return cls.build("SUCCESS", data)


class BaseView(object):
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
                return "POST_FORMAT_ERR", "LACK PARAMS_REQUIRED: " + _field
            elif not _check_data_type(self.url_params.get(_field), _type):
                return "POST_FORMAT_ERR", "PARAM [%s] DATA TYPE ERROR : %s" % (_field, _type)
        return None

    # 检查post数据的完整性
    def check_post(self, post_frame={}):
        for name, value in post_frame.items():
            data = self.post_body.get(name)
            if data is None:  # level 1
                return "POST_FORMAT_ERR", "LACK POST FIELD:" + name
            if type_util.is_dict(value):
                if not type_util.is_dict(data):
                    return "POST_FORMAT_ERR", "Error POST FIELD Type (%s) MUST BE  A DICT" % (name)

                for key, val in value.items():
                    data_val = data.get(key)
                    if data_val is None:  # level 2
                        return "POST_FORMAT_ERR", "LACK POST FIELD:%s.%s" % (name, key)
                    if type_util.is_dict(val):
                        if not type_util.is_dict(data_val):
                            return "POST_FORMAT_ERR", "Error POST FIELD Type (%s.%s) MUST BE  A DICT" % (name, key)

                        for k, v in val.items():
                            data_v = data_val.get(k)
                            if data_v is None:  # level 3
                                return "POST_FORMAT_ERR", "LACK POST FIELD:%s.%s.%s" % (name, key, k)
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

    # 把分页器转为切片器
    def parse_limit(self):
        page_no = int(self.url_params.get("page_no") or 0)
        if page_no < 0:
            page_no = 0

        page_size = int(self.url_params.get("page_size") or 500)
        if page_size < 0 or page_size > 500:
            page_size = 500

        start = page_no * page_size
        end = (page_no + 1) * page_size
        limit = (start, end)

        return limit


class GeneralView(BaseView, APIView,):
    pass


class NoLoginView(BaseView, APIView):
    pass


class WeChatView(BaseView, APIView):
    pass

