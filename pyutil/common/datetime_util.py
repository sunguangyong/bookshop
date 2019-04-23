#!/usr/bin/python
#-*- coding:utf-8 -*-

import time, datetime
import struct

from functools import wraps

def DaysMonth(year,month):
    days_month = [31,28,31,30,31,30,31,31,30,31,30,31]
    if ((year%4==0 and year%100 != 0) or year%400 == 0):
        days_month[1] = 29
    return days_month[month]

def time_call(func):
    @wraps(func)
    def wrap_call(*args, **kwargs):
        start = time.time()
        res = func(*args, **kwargs)
        end = time.time()
        print "Call", func.__name__, "Cost", end-start
        return res
    return wrap_call

def TimeSeconds(time_stamp):
    time_arr = time.strptime(time_stamp, "%Y-%m-%d %H:%M:%S")
    return int(time.mktime(time_arr))

def TimeNow():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))

def SecondToTime(seconds):
    return time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(seconds))

def NowSeconds():
    return int(time.time())

def NowDatetime():
    return datetime.datetime.now() 

def TimeBeforeNow(seconds):
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()-int(seconds)))

def TimeAfterNow(seconds):
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()+int(seconds)))

def DaysBeforeNow(days):
    seconds = 3600*24*days
    return TimeBeforeNow(seconds)

def DaysAfterNow(days):
    seconds = 3600*24*days
    return TimeAfterNow(seconds)

def TimeStampBefore(time_stamp, seconds):
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(TimeSeconds(time_stamp)-int(seconds)))

def TimeStampAfter(time_stamp, seconds):
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(TimeSeconds(time_stamp)+int(seconds)))

def Datetime2Int(date_time):
    return time.mktime(date_time.timetuple())

def Datetime2String(date_time):
    return date_time.strftime('%Y-%m-%d %H:%M:%S')

def String2Time(time_str):
    return time.strptime(time_str, '%Y-%m-%d %H:%M:%S')

def String2Datetime(time_str):
    return datetime.datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S')

def TimeBCD():
    timestr = TimeNow()
    year = struct.pack("B", int(timestr[2:4]))
    mon = struct.pack("B", int(timestr[5:7]))
    day = struct.pack("B", int(timestr[8:10]))
    hour = struct.pack("B", int(timestr[11:13]))
    min = struct.pack("B", int(timestr[14:16]))
    sec = struct.pack("B", int(timestr[17:19]))
    return sec+min+hour+day+mon+year


def FirstDay2Month(month_delta=0):
    # 获取当月第一天，month_delta = -1， 上个月第一天，month_delta=1， 下个月第一天
    curTime = datetime.date.today()
    year_delta = 0
    if month_delta + curTime.month > 12 or month_delta + curTime.month < 1:
        year_delta = (month_delta + curTime.month) / 12
        month_delta = month_delta - (month_delta + curTime.month) / 12 * 12
    firstDay = datetime.datetime(year=curTime.year + year_delta, month=curTime.month + month_delta, day=1, hour=0, minute=0, second=0)
    return firstDay


def LastDay2Month(month_delta=-1):
    # 获取当月最后一天
    lastMonthFirstDay = FirstDay2Month(month_delta = month_delta + 1)
    lastDay = lastMonthFirstDay - datetime.timedelta(days = 1)
    return lastDay.replace(hour=23, minute=59, second=59)


def FirstDay2Week(week_delta=0):
    # 获取当周的第一天（周一）
    weekNum = datetime.datetime.now().weekday()
    Monday = datetime.datetime.now() + datetime.timedelta(days=-weekNum+week_delta*7)
    return Monday.replace(hour=0, minute=0, second=0, microsecond=0)


def LastDay2Week(week_delta=-1):
    # 获取当周的最后一天（周日）
    weekNum = datetime.datetime.now().weekday()
    Sunday = datetime.datetime.now() + datetime.timedelta(days = week_delta * 7 + 6 - weekNum)
    return Sunday.replace(hour=23, minute=59, second=59, microsecond=0)


def LastDay(days=-1):
    return (datetime.datetime.now() + datetime.timedelta(days=days)).replace(hour=0, minute=0, second=0, microsecond=0)


def MonthBefore(month_before=1):
    # 返回month_before个自然月前第一天日期
    time_now = datetime.datetime.now()
    time_now = datetime.datetime(time_now.year, time_now.month, 1, 0, 0, 0)
    year = time_now.year
    month = time_now.month
    days = 0
    while month_before > 0:
        if (month-1) <= 0:
            year -= 1
            month = 12
        month -= 1
        days += DaysMonth(year, month)
        month_before -= 1
    return time_now - datetime.timedelta(days=days)


def YearBefore(year_before=1):
    # 返回year_before个自然年前第一天日期
    year = datetime.datetime.now().year
    return datetime.datetime(year - year_before, 1, 1, 0, 0, 0)


def DateTimeFormat(date_time, format_string="%Y-%m-%d %H:%M:%S"):
    # 将时间格式化
    if not date_time:
        date_time = datetime.datetime.now()
    return date_time.strftime(format_string)


if __name__ == '__main__':
    d = datetime.datetime.now()
    print Datetime2String(d)
    print TimeNow()
    print TimeStampBefore("2017-12-11 12:00:00", 59)
    print TimeBeforeNow(30)
    print SecondToTime(1489991675)
    print FirstDay2Month(-12 + 1)
    print LastDay2Month(0), LastDay2Month(-2)
    print FirstDay2Week(), FirstDay2Week(-2)
    print LastDay2Week(-2), LastDay2Week(0)
    print LastDay(), LastDay(-2)
