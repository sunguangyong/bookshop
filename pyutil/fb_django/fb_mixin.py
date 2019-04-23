#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pyutil.common.sys_utf8
import pyutil.common.ip_util as ip_util
import pyutil.common.md5_util as md5_util
import pyutil.common.datetime_util as dt_util
import pyutil.fb_django.fb_auth as fb_auth
from pyutil.fb_django.fb_error import ResponseCode 
from django.shortcuts import HttpResponse

from common_api.manna.auth.authority import Auth

import json
import re
import base64
import urllib
import logging 
logger = logging.getLogger(__name__)

'''IP白名单'''
_ip_white_list = ["127.0.0.1", "172.16.15.240", "172.16.15.252", "172.16.15.243"]
_local_ip_pattern = r"^172\.16\.\d{1,3}.\d{1,3}$"
_sign_key = "Fubang.119*("
_sign_keys_pattern = r'^,(\s[^ ]+){3,}$'

# sign过期时间(单位是秒)
_sign_expired = 60 * 60 * 24 * 30 * 12

# 版本号格式
_cv_pattern = r"FB(\d{1,2}\.\d{1,2}\.\d{1,2}\.\d{2})_([AIW])\d\.\d"

_default_page = 0
_default_page_size = 50

_start_token = False 

_start_permission = False

_start_local_net = True #开启内网访问不校验原子封装

# 客户端请求合法验证
class RequestMixin(object):

    def dispatch(self, request, *args, **kwargs):    
        self.url_params = {} 
        self.post_body = {} 
        self.fetch_get_params(request)
        self.fetch_post_params(request)
        #设置默认值
        self.set_default_value()
        self.build_params(request)

        if self.check(request):
            return super(RequestMixin, self).dispatch(request, *args, **kwargs)
        else:
            return HttpResponse(json.dumps(
                ResponseCode.build("ILLEGAL")),
                content_type="application/json")

    def check(self, request):
        if self.JU_CLIENT_IP in _ip_white_list:
            return True
        if _start_local_net and re.match(_local_ip_pattern, self.JU_CLIENT_IP) is not None:
            return True

        return self.check_atom(request) and self.check_sign(request)
   

    def build_params(self, request):
        cv = self.url_params.get('cv',"")
        self.JU_PLATFORM = "WEB"
        self.JU_CLIENT_IP = ip_util.get_http_ip(request) 
        matchObj = re.match(_cv_pattern,cv)
        if matchObj is not None:
            self.JU_VERSION = matchObj.group(1)
            _p = matchObj.group(2)
            if _p == "A":
                self.JU_PLATFORM = "ANDROID"
            elif _p == "I":
                self.JU_PLATFORM = "IOS"


    def check_atom(self, request):
        cv = self.url_params.get('cv')
        ua = self.url_params.get('ua')
         
        sign_time = self.url_params.get('sign_time')
        sign_random = self.url_params.get('sign_random')
        sign = self.url_params.get('sign')

        if cv is None or ua is None or \
            sign_time is None or sign_random is None or \
            sign is None:
            return False
        
        # 时间戳比较时差
        if len(sign_time)!= 10 or dt_util.NowSeconds() - int(sign_time) > _sign_expired:
            return False
        
        return True



    def check_sign(self, request):
        sign = self.url_params.get('sign')
        
        if sign is None or sign == "":
            return False

        sign_keys_str = base64.b64decode(request.GET.get('sign_keys'))
        if re.match(_sign_keys_pattern, sign_keys_str) is None:
            return False

        sign_keys = sign_keys_str.split(" ")
        if "sign_time" not in sign_keys:
            return False
        
        temp_str = "sign_key="+_sign_key
        for key in sign_keys:
            if key == ",":
                continue

            value = self.url_params.get(key)
            if value is None:
                return False
            else:
                temp_str += "&" + key + "=" + value
        md5_str = md5_util.md5(temp_str).upper()
        if sign == md5_str:
            return True
        else:
            return False

    
    def fetch_get_params(self,request):
        '''parse get params to dict'''
        for key in request.GET.keys():
           self.url_params[key] = request.GET.get(key)     
        return     
    
    def fetch_post_params(self,request):
        '''parse post params'''
        if request and request.body:
            self.raw_post_body = request.body
            try:
                self.post_body = json.loads(request.body)
            except:
                self.post_body = json.loads(urllib.unquote_plus(request.body))
        return 

    def set_default_value(self):
        self.default_page = _default_page 
        self.default_page_size = _default_page_size 



#登录信息的验证
class LoginMixin(object):
    
    def dispatch(self, request, *args, **kwargs):    

        token = fb_auth.get_token(request)
        if token and fb_auth.check_token(token):
            
            payload = fb_auth.get_payload(token)
            self.JU_USER_ID = payload.get("user_id") 
            self.JU_USER_TYPE = payload.get("user_type") 
            self.JU_USER_ROLE = payload.get("user_role") 
            return super(LoginMixin, self).dispatch(request, *args, **kwargs)
        elif _start_token == False:
            return super(LoginMixin, self).dispatch(request, *args, **kwargs)
        else:
            return HttpResponse(json.dumps(
                ResponseCode.build("TOKEN_ERR")),
                content_type="application/json")



#接口权限的验证
class PermissionMixin(object):
    def dispatch(self, request, *args, **kwargs):    
        uid = self.url_params.get("uid")
        url = request.path.replace("/fe/", "/")
        operation = "r" if request.method == "GET" else "w"
        if _start_permission == False:
            return super(PermissionMixin, self).dispatch(request, *args, **kwargs)
        elif Auth.check(uid, url, operation):
            return super(PermissionMixin, self).dispatch(request, *args, **kwargs)
        else:
            return HttpResponse(json.dumps(
                ResponseCode.build("AUTH_ERR")),
                content_type="application/json")

    def __check_api(url, user_id, user_type_id, user_role_id):
        return True
