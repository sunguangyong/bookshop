
from pyutil.nsq.nsqer import NsqWriter
from pyutil.nsq.config import conf_ol

nsqer = NsqWriter(conf_ol.config["nsqd_http_hosts"], "topic_maint_notation")
msg = {}
nsqer.produce(json.dumps(msg))
