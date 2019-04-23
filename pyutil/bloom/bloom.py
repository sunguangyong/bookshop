#!/usr/bin/env python
# -*- coding: utf-8 -*-
#create by basearch@fubang

from requests import Session
import pyutil.common.dict_util as dict_util
import pyutil.common.token_util as token_util
import json




"""
  自研的推送接口
"""
class Bloomer(object):
    PIPE_WS = 1  #websocket
    PIPE_JG = 2  #极光
    PIPE_WS_JG = 3 #websocket和极光

    def __init__(self, product_id, app_id, url="http://push.fubangyun.cn:18888/gateway/pushMsg"):
        self.url = url
        self.session = Session()
        self.Data = dict_util.Dict(*("product_id",
                            "app_id",
                            "group_id",
                            "pipe",
                            "data"))
        self.Data.product_id = int(product_id)
        self.Data.app_id = int(app_id)

    def push_msg(self, group_id, msg, pipe=Bloomer.PIPE_WS):
        self.Data.data = msg
        self.Data.pipe = int(pipe)
        self.Data.group_id = str(group_id)
        return self.session.post(self.url, json.dumps(self.Data()))

class Grouper(object):
    def __init__(self, product_id, app_id, url="http://push.fubangyun.cn:18888/gateway/addGroup"):
        self.url = url
        self.session = Session()
        self.Data = dict_util.Dict(*("product_id",
                                     "app_id",
                                     "group_id",
                                     "user_id",
                                     "accesstoken"))
        self.Data.product_id = int(product_id)
        self.Data.app_id = int(app_id)

    def add_group(self, group_id):
        self.Data.group_id = str(group_id)
        self.Data.accesstoken = token_util.gen_token()
        return self.session.post(self.url, json.dumps(self.Data()))

class User(object):

    def __init__(self, product_id, app_id, url="http://push.fubangyun.cn:18888/gateway/addUser"):
        self.url = url
        self.session = Session()
        self.Data = dict_util.Dict(*("product_id",
                                     "app_id",
                                     "group_id",
                                     "accesstoken"))

        self.Data.product_id = product_id
        self.Data.app_id = app_id

    def add_user(self, group_id, user_id):
        self.Data.group_id = str(group_id)
        self.Data.user_id = [str(id) for id in user_id] if isinstance(user_id, list) else [str(user_id),]
        return self.session.post(self.url, json.dumps(self.Data()))

def test():
    grouper = Grouper(url="http://push.fubangyun.cn:18888/gateway/addGroup", product_id=2, app_id=5)
    result = grouper.add_group("2512345678").text
    print "after add group:", result

    user = User(product_id=2, app_id=5)
    result = user.add_user("2512345678", [665,666,234,567,233]).text
    print "after add user:", result

    bloomer = Bloomer(product_id=2, app_id=5)
    result = bloomer.push_msg("2512345678", 0, "hello, world, I am fubang drogher~~").text
    print "after add bloomer:", result


if __name__ == '__main__':
    test()
