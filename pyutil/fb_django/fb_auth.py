#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.core import signing
import hashlib
from django.core.cache import cache
from pyutil.fb_redis.redis_cache import redis_cache
import pyconf.redis.redis as redis_conf
import pyutil.common.datetime_util as date_time

HEADER = {'typ': 'JWP', 'alg': 'default'}
KEY = 'Fubang.119*('
SALT = 'fubangyun.com'
CACHE_TIME_OUT = 60 * 60 * 24 * 5  # 24h * 5
REDIS_KEY = "TOKEN_USER:%s:%s"

REDIS_CACHE  = redis_cache(config_dic = redis_conf.config)

PLATFORM_LIST = ["WEB", "IOS", "ANDROID"]

"""
用户登录限制
单个平台只能登录一个账号: TOKEN_USER:WEB:12345
"""


def encrypt(obj):
    """加密"""
    value = signing.dumps(obj, key=KEY, salt=SALT)
    value = signing.b64_encode(value.encode()).decode()
    return value


def decrypt(src):
    """解密"""
    src = signing.b64_decode(src.encode()).decode()
    raw = signing.loads(src, key=KEY, salt=SALT)
    return raw


def create_token(user_type, user_role, user_id, platform="WEB"):
    """生成token信息"""
    # 1. 加密头信息
    header = encrypt(HEADER)
    # 2. 构造Payload
    payload =  __build_payload(user_type, user_role, user_id, platform)
    payload = encrypt(payload)
    # 3. 生成签名
    md5 = hashlib.md5()
    md5.update(("%s.%s" % (header, payload)).encode())
    signature = md5.hexdigest()
    token = "%s.%s.%s" % (header, payload, signature)

    # redis 缓存
    CACHE_KEY = __build_cache_key(user_id, platform)
    
    REDIS_CACHE.put_to_cache_ex(CACHE_KEY, token, CACHE_TIME_OUT)
    return token


def get_payload(token):
    payload = str(token).split('.')[1]
    payload = decrypt(payload)
    return payload



def check_token(token):
    if len(str(token).split('.')) == 3:
        CACHE_KEY = __get_cache_key(token)
        last_token = REDIS_CACHE.get_from_cache(CACHE_KEY)
        if last_token:
            return last_token == token
    return False



def del_token(token):
    CACHE_KEY = __get_cache_key(token)
    REDIS_CACHE.del_from_cache(CACHE_KEY)


def del_token_by_user(user_id, platform="ALL"):
    def _del(_user_id, _platform):
        REDIS_CACHE.del_from_cache(__build_cache_key(_user_id, _platform))
    
    if platform in PLATFORM_LIST:
       _del(user_id, platform) 
    elif platform == "ALL":
        for pm in PLATFORM_LIST:
            _del(user_id, pm) 


def get_token(request):
    if not request or not request.META:
        return None
    token = request.META.get("HTTP_AUTHORIZATION", None)
    token = token if token is None or len(token.split(' '))< 2 else token.split(' ')[1]
    return token


def __get_cache_key(token):
    payload = get_payload(token)
    user_id = payload.get("user_id")
    platform = payload.get("platform")
    return  REDIS_KEY % (platform, user_id)


def __build_payload(user_type, user_role, user_id, platform):
    return {"user_id": user_id, "user_type": user_type, "user_role" : user_role,\
            "platform" : platform, "iat": date_time.NowSeconds()}


def __build_cache_key(user_id, platform):
    return REDIS_KEY % (platform, user_id)




if __name__ ==  "__main__":
    
    create_token(1)
    
    print check_token("ZXlKaGJHY2lPaUprWldaaGRXeDBJaXdpZEhsd0lqb2lTbGRRSW4wOjFmaXQ2ODpWVVRlVHpmMWxra3ZFSHE1dE9iU3RqTjk3Qlk.ZXlKcFlYUWlPakUxTXpJMk5qQTROREF1TlRjM09URXhMQ0oxYzJWeVgybGtJam94ZlE6MWZpdDY4Oi1mMzRCQmFZWExuUmg3SWFWcURiQ1o0blpuOA.86376d439039c5755276a28a89cd4cf2")
    del_token("ZXlKaGJHY2lPaUprWldaaGRXeDBJaXdpZEhsd0lqb2lTbGRRSW4wOjFmaXQ2ODpWVVRlVHpmMWxra3ZFSHE1dE9iU3RqTjk3Qlk.ZXlKcFlYUWlPakUxTXpJMk5qQTROREF1TlRjM09URXhMQ0oxYzJWeVgybGtJam94ZlE6MWZpdDY4Oi1mMzRCQmFZWExuUmg3SWFWcURiQ1o0blpuOA.86376d439039c5755276a28a89cd4cf2")
