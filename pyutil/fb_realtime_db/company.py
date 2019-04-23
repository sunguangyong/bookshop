
import pyutil.db.mellow as mellow
import pyconf.db.realtime_db as realtime_db

mysql = mellow.mellow(realtime_db.config)

class company:

    @classmethod
    def get_building_ids(cls, company_id):
        building_ids = []
        for row in mysql.Find("relation_company_building", ["building_id",], {"company_id": company_id}, out=list): 
            if not row[0]:
                continue
            building_ids.append(row[0])
        return building_ids


    @classmethod
    def get_center_ids(cls, company_id):
        center_ids = []
        for row in mysql.Find("relation_company_center", ["center_id",], {"company_id": company_id}, out=list): 
            if not row[0]:
                continue
            center_ids.append(row[0])
        return center_ids
     

    @classmethod
    def get_dtu_ids(cls, company_id):
        all = []
        all.extend(mysql.Find("relation_company_dtu", ["dtu_id", '"dtu"'], {"company_id": company_id}))
        all.extend(mysql.Find("relation_company_manometer", ["manometer_id",'"manometer"' ], {"company_id": company_id}))
        all.extend(mysql.Find("relation_company_water_level", ["dtu_id", '"water_level"'], {"company_id": company_id}))
        return all


    @classmethod
    def get_device_ids(cls, company_id):
        devices = []
        for dtu in cls.get_dtu_ids(company_id): 
            dtu_id = dtu[0]
            for row in mysql.Find("info_component", ["component_code"], {"dtu_id": dtu_id}):
                dev = {"id":int(row[0]), "type":"device"}
                devices.append(dev)

        for row in mysql.Find("info_manometer", ["id"], {"company_id": company_id}):
            dev = {"id":row[0], "type":"manometer"}
            devices.append(dev)

        for row in mysql.Find("info_water_level", ["id"], {"company_id": company_id}):
            dev = {"id":int(row[0]), "type":"water_level"}
            devices.append(dev)
        return devices


if __name__ == '__main__':
    print company().get_device_ids(1210000757)
