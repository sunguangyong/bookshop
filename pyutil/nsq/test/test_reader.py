#encoding:utf-8


import pyutil.nsq.config.conf_ol as conf_ol
import pyutil.nsq.nsqer as nsqer


def handler(msg):
    print msg.id, msg.body
    return True

if __name__ == '__main__':
    reader = nsqer.NsqReader(conf_ol.config["nsqlookupd_http_hosts"], "test_nsq_by_zhc", "zhc_chan1", handler)
    reader.run()
