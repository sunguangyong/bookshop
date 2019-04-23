# -*- coding: utf-8 -*- 

import json
import pyutil.db.mellow as mellow
import openapi.config.dbconfig_realtime_shenyang as dbconfig_realtime_shenyang
#import openapi.config.dbconfig_iot119 as dbconfig_iot119


class component():
    def __init__(self):

        self.class_name = self.__class__.__name__
        self.mysql = mellow.mellow(dbconfig_realtime_shenyang.config)

    def run(self):
        dtuid_companyid_map = {}
        rows = self.mysql.Find("relation_company_dtu", ["company_id", "dtu_id"])
        for row in rows:
            dtuid_companyid_map[row[1]] = row[0]

        rows = self.mysql.Find("relation_company_manometer", ["company_id", "manometer_id"])
        for row in rows:
            dtuid_companyid_map[row[1]] = row[0]

        rows = self.mysql.Find("relation_company_water_level", ["company_id", "dtu_id"])
        for row in rows:
            dtuid_companyid_map[row[1]] = row[0]

        for dtu_id, company_id in dtuid_companyid_map.items():
            if not dtu_id or not company_id:
                continue
            self.mysql.Update("info_component", {"company_id": company_id}, {"dtu_id":dtu_id}) 
            self.mysql.Update("info_manometer", {"company_id": company_id}, {"id":dtu_id}) 
            self.mysql.Update("info_water_level", {"company_id": company_id}, {"id":dtu_id}) 


if __name__ == '__main__':
    component().run()
