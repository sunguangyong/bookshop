#!/usr/bin/python
#-*- coding:utf-8 -*-

import time, datetime

def GenPercent(numbers):
    '''
    @param: numbers a list of int
    @return: result a list of percentage 
    '''
    if len(numbers)<1 :
        return False
    s = sum(numbers)
    percent = [float(x*100)/s for x in numbers]
    r = [int(round(x)) for x in percent]
    decimal = [(percent[x]-r[x],x) for x in range(len(r))]
    modifier = 100 - sum(r)
    if modifier > 0:
        decimal = sorted(decimal, reverse=True)
        for i in range(modifier):
            r[decimal[i][1]] = r[decimal[i][1]] + 1
    elif modifier < 0:
        decimal = sorted(decimal)
        for i in range(-1*modifier):
            r[decimal[i][1]] = r[decimal[i][1]] -1
    return r
    

if __name__ == '__main__':
    data = [214, 224, 334, 228]
    import sys
    print GenPercent([int(x) for x in sys.argv[1:]])
