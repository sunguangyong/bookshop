# coding=utf-8


from pyutil.fb_jpush.jpush_conf import APPKEY, MASTERSECRET, IS_IOS_DEV

import jpush as jpush
from jpush import common


class SendPush(object):
    """
    send message by jiguang SDK
    """

    def __new__(cls, *args, **kwargs):
        app_key = args[0]
        master_secret = args[1]
        if not hasattr(SendPush, '_instance'):
            obj = super(SendPush, cls).__new__(cls, *args, **kwargs)
            obj.jpush = jpush.JPush(app_key, master_secret)
            obj.jpush.set_logging('DEBUG')
            cls._instance = obj
        return cls._instance

    def __init__(self, app_key, master_secret):
        self.app_key = app_key
        self.master_secret = master_secret
        self.push = self.jpush.create_push()

    def all(self, tagname, msg):
        """
        send message to all device
        """
        self.push.audience = jpush.all_
        self.push.notification = jpush.notification(alert=msg)
        self.push.platform = jpush.all_
        try:
            response = self.push.send()
            print '==========', response
        except common.Unauthorized:
            raise common.Unauthorized("Unauthorized")
        except common.APIConnectionException:
            raise common.APIConnectionException("conn")
        except common.JPushFailure:
            print ("JPushFailure")
        except:
            print ("Exception")

    def iso_android(self, tagname, msg):
        """
        just send message to iso and android
        :param tagname:
        :param msg:
        :return:
        """
        try:
            ios = jpush.ios(alert=str(msg), sound='default')
            android = jpush.android(alert=str(msg))

            self.push.audience = jpush.audience(jpush.tag(tagname))
            self.push.notification = jpush.notification(alert=str(msg), android=android, ios=ios)
            self.push.options = {"time_to_live": 86400, "apns_production": IS_IOS_DEV}
            self.push.platform = jpush.all_
            try:
                response = self.push.send()
                print 'IOS_ANDROID RESPONSE>>>', response
            except Exception, e:
                print 'IOS_ANDROID ERROR>>>', e
        except:
            pass


jpusher = SendPush(APPKEY, MASTERSECRET)

if __name__ == '__main__':
    sendpush = SendPush(APPKEY, MASTERSECRET)
    sendpush.iso_android("2_233", 'hello')
