
#!/usr/bin/python
#-*- coding:utf-8 -*-

import md5 as md5lib

def md5(s):
    m = md5lib.new()
    m.update(s)
    return m.hexdigest()

if __name__ == '__main__':
    print md5("12334")
