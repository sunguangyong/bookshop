# -*- coding: utf-8 -*- 

import json
import pyutil.db.mellow as mellow
import pyconf.db.manna as manna
import pyconf.db.realtime_db as realtime_db


class info_device_dtu():
    def __init__(self):
        self.mysql = mellow.mellow(manna.config)
        self.mysql_old = mellow.mellow(realtime_db.config)
        self.dtu_protocol_map = {}

    def run(self):
        dtu_map = {}
        for record in self.mysql.Find("info_device", [], {"thing_type":"info_device_alarmer"},out=dict):
            dtu_map[record["thing_id"]] = record["enum_device_model"]

        for record in self.mysql.Find("info_device_alarmer",[], out=dict):
            dtu_id = record["dtu_id"]
            alarmer_id = record["alarmer_id"]
            enum_host_protocol = dtu_map.get(alarmer_id, -1)
            print dtu_id, enum_host_protocol
            self.mysql.Update("info_device_dtu", {"enum_host_protocol": enum_host_protocol}, {"dtu_id":dtu_id})
            self.dtu_protocol_map[dtu_id] = enum_host_protocol

    def run_old(self):
        for record in self.mysql_old.Find("info_dtu", out=dict):
            dtu_id = record["id"]
            enum_host_protocol = record.get("controller_protocol_id", -1) #TODO
            if enum_host_protocol <=0:
                enum_host_protocol = -1
            else:
                enum_host_protocol += 200000
            print dtu_id, enum_host_protocol
            self.mysql.Update("info_device_dtu", {"enum_host_protocol": enum_host_protocol}, {"dtu_id":dtu_id})


if __name__ == '__main__':
    info_device_dtu().run_old()
