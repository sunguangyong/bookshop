#!/usr/bin/python
#-*- coding:utf-8 -*-

def hexShow(argv):
    result = ''
    hLen = len(argv)
    for i in xrange(hLen):
        hvol = ord(argv[i])
        hhex = '%02x'%hvol
        result += hhex+' '
    #print 'hexShow:',result
    return result

