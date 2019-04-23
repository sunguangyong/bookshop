# -*- coding: utf-8 -*- 

import random
import httplib
import time
import nsq
import json


class NsqWriter():
    def __init__(self, hosts, topic):
        self.addrs = hosts
        self.topic = topic
        self.conn = None
        self.n = 0
        self.lasttime = 0.0
        self.__rebuild_conn()

    def __rebuild_conn(self):
        if self.conn:
            self.conn.close()

        ip, port = random.choice(self.addrs).split(":")
        print "build connection: ", ip, ":", port
        self.conn = httplib.HTTPConnection(ip, int(port))
        self.lasttime = time.time()

    def __inc_n(self, num):
        self.n += num
        if self.n % 200 ==0 or time.time()-self.lasttime>30:
            self.__rebuild_conn()
        self.lasttime = time.time()

    def produce(self, msg):
        if not msg:
            print "Error, call produce, msg:", msg
            return
        try:
            self.__inc_n(1)
            self.conn.request("POST", "/pub?topic="+self.topic, msg, {"Contention":"Keep-Alive"})
            response = self.conn.getresponse()
            print response.read(), self.topic
        except Exception, e:
            print "Exception: ", e
            self.__rebuild_conn()

    def mproduce(self, msgs):
        if not msgs or not ( isinstance(msgs, list) or isinstance(msgs, tuple) ):
            print "ERROR: call mproduct, msgs=", msgs
            return
        try:
            self.__inc_n(1)
            result = []
            for msg in msgs:
                result.append(json.dumps(msg) if isinstance(msg, dict) else str(msg)) 
            self.conn.request("POST", "/mpub?topic="+self.topic, '\n'.join(result), {"Contention":"Keep-Alive"})
            response = self.conn.getresponse()
            print response.read()
        except Exception, e:
            print "Exception: ", e
            self.__rebuild_conn()
 
class NsqReader():
    def __init__(self, lookupd_http_addresses, topic, channel, handler):
        self.r = nsq.Reader(message_handler=handler, 
            lookupd_http_addresses=lookupd_http_addresses, 
            topic=topic, channel=channel, max_in_flight=5)

    def run(self):
        nsq.run()


if __name__ == "__main__":
   pass 
