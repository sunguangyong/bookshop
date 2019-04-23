#!/usr/bin/python
# -*- coding:utf-8 -*-

import socket
import struct
import fcntl


def get_ip(ethname="eth0"):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        ip = socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0X8915, struct.pack('256s', ethname[:15]))[20:24])
    except Exception as e:
        ip = socket.gethostbyname(socket.gethostname())
    return ip


def get_http_ip(request):
    if request.META.has_key('HTTP_X_FORWARDED_FOR'):
        ip = request.META['HTTP_X_FORWARDED_FOR']
    else:
        ip = request.META['REMOTE_ADDR']
    return ip
