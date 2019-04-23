# -*- coding: utf-8 -*- 

import json

SUCCESS = 0
FAIL = 1
NOTEXIST = 2
INVALID_OPERATION = 3
LACK_PARAMS = 6
LOGIN_INVALID = 7
LACK_ID = 8

ERROR_MAP = {
    SUCCESS: "SUCCESS",
    FAIL: "FAILED",
    NOTEXIST: "Device not Exist",
    INVALID_OPERATION: "Invalid Operation",
    LACK_PARAMS: "lack params",
    LOGIN_INVALID: "login invalid",
    LACK_ID: "LACK_ID",
}

def FlaskPostJson():
    from flask import request

    print "FORM===", request.form.items(), "||||||request.data=", request.data, "||||||request.json=", request.json

    post = request.data
    if len(request.form)>0:
        post = ""

    for item in request.form.items():
        post += item[0]

    return json.loads(post)

def FlaskResponse(data, code=0, msg=""):
    if not msg:
        msg = ERROR_MAP.get(code) or ""
    return json.dumps({"code": code, "msg": msg, "data": data})

