# -*- coding: utf-8 -*- 
'''
created by zhhliu @ 2018年6月19日
本模块用于产生模拟报警数据，测试系统功能
'''

import sys
import json
import time
from pyutil.common.datetime_util import TimeNow 
from pyutil.nsq.nsqer import NsqWriter
import random

class NsqMsg():
    def __init__(self, nsqd_hosts):
        self.rt_event = NsqWriter(nsqd_hosts, "rt_event")
        self.rt_packet = NsqWriter(nsqd_hosts, "rt_packet")
        self.rt_analog = NsqWriter(nsqd_hosts, "rt_analog")

    def PushMsg(self, topic, msg):
        '''
        将序列化后的消息推送到指定的topic
        '''
        if topic == "rt_event":
            self.rt_event.produce(msg)
        elif topic == "rt_analog":
            self.rt_analog.produce(msg)
        else:
            self.rt_packet.produce(msg)

    def GenEvent(self, dtuId, loopNumber=0, componentNumber=0, componentType=0, statusId=0, value=0, valueType=0, valueOrig="", componentCode=0, hostTime="", alarmerId=0):
        '''
        根据给定的参数来产生消息
        '''
        data = {
            "uuid": "aaa",
            "dtuId": dtuId,
            "alarmHostId": 0,
            "thingId": int("%d%03d%03d%03d"%(dtuId%100000000, loopNumber%1000, componentNumber%1000, 0)),
            "componentCode": int("%03d%03d"%(loopNumber%1000, componentNumber%1000)),
            "thingType": "info_device_component",
            "thingTypeId": componentType,
            "statusId": statusId,
            "position": "",
            "receiveTime": TimeNow(),
            "hostTime": TimeNow(),
            "value": value,
            "valueOrig": valueOrig,
            "valueType": valueType,
            "loopNumber": loopNumber,
            "componentNumber": componentNumber,
            "protocol": "demo_monit",
            "errorCode": 1,
        }
        if componentCode > 0:
            data["componentCode"] = componentCode
        if len(hostTime) > 0:
            data["hostTime"] = hostTime
        if alarmerId > 0:
            data["alarmHostId"] = alarmerId
        msg = json.dumps(data)
        self.rt_event.produce(msg)
        print "produce rt_event ", msg
        return msg

    def GenAnalog(self, dtuId, loopNumber=0, componentNumber=0, componentType=0, value=0, valueType=0, valueOrig=0, componentCode=0):
        '''
        根据给定的参数来产生ananlog消息
        '''
        data = {
        "uuid": "aaa",
        "dtuId": dtuId,
        "alarmHostId": 0,        
        "thingId": int("%d%03d%03d%03d"%(dtuId%100000000, loopNumber%1000, componentNumber%1000, 0)),
        "componentCode": int("%03d%03d"%(loopNumber%1000, componentNumber%1000)),  
        "thingType": "info_device_component",
        "thingTypeId": componentType,
        "statusId": 1,
        "position": "",
        "receiveTime": TimeNow(),
        "hostTime": TimeNow(),
        "value":value,
        "valueOrig": valueOrig,
        "valueType": valueType,
        "loopNumber": loopNumber,
        "componentNumber": componentNumber,
        "protocol": "demo_monit",
        "errorCode": 1,
        }
        if componentCode > 0:
            data["componentCode"] = componentCode
        msg = json.dumps(data)
        self.rt_analog.produce(msg)
        print "produce rt_analog, ", msg
        return msg

    def GenPacket(self, dtuId):
        '''
        根据给定的参数来产生packet的消息
        '''
        data = {
        "uuid": "aaa",
        "dtuId": dtuId,
        "thingId": 0,
        "thingType": "info_device_component",
        "data": "",
        "packetType": "heartbeat",
        "receiveTime": TimeNow(),
        "hostTime": TimeNow(),
        }
        msg = json.dumps(data)
        self.rt_packet.produce(msg)
        print "produce rt_packet, ", msg
        return msg


if __name__=="__main__":
    msg = NsqMsg(["172.16.15.244:4151", "172.16.15.244:4251", "172.16.15.245:4151", "172.16.15.245:4251"])
    msg.GenPacket(1234567654321)
    msg.GenEvent(1234567654321, 2, 2, 40, 2, 0, 0)
    msg.GenAnalog(1234567654321, 2, 2, 17, 360, 3)


