#encoding:utf-8


import pyutil.nsq.config.conf_ol as conf_ol
import pyutil.nsq.nsqer as nsqer


if __name__ == '__main__':
    writer = nsqer.NsqWriter(conf_ol.config["nsqd_http_hosts"], "test_nsq_by_zhc")
    writer.produce("hello, zhc, msg001")
