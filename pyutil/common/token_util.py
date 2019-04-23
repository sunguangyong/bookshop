#!/usr/bin/python
#-*- coding:utf-8 -*-

import os
import uuid


def gen_token():
    return uuid.uuid4().hex

def test():
    print gen_token()

if __name__ == '__main__':
    test()
