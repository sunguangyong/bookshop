
import pyutil.db.mellow as mellow
import pyconf.db.realtime_db as realtime_db
import pyutil.fb_realtime_db.company as fb_company

mysql = mellow.mellow(realtime_db.config)

class dtu:

    @classmethod
    def get_center_id(cls, dtu_id, dtu_type):
        company_id = cls.get_company_cared_id(dtu_id, dtu_type)
        center_ids = fb_company.company.get_center_ids(company_id)
        return center_ids[0] if center_ids else -1
        
    @classmethod
    def get_building_id(cls, dtu_id, dtu_type):
        company_id = cls.get_company_cared_id(dtu_id, dtu_type)
        ids = fb_company.company.get_building_ids(company_id)
        return ids[0] if ids else -1

    @classmethod
    def get_company_cared_id(cls, dtu_id, dtu_type):
        if dtu_type == "dtu":
            rows = mysql.Find("relation_company_dtu", ["company_id"], {"dtu_id": dtu_id}) or []
            return rows[0][0] if rows else -1
        elif dtu_type  == "manometer":
            rows = mysql.Find("relation_company_manometer", ["company_id"], {"dtu_id": dtu_id}) or []
            return rows[0][0] if rows else -1
        elif dtu_type  == "water_level":
            rows = mysql.Find("relation_company_water_level", ["company_id"], {"dtu_id": dtu_id}) or []
            return rows[0][0] if rows else -1
        else:
            print "Error, dtu_type not recognized, dtu_type=", dtu_type
            return -1


    @classmethod
    def get_company_authority_id(cls, dtu_id, dtu_type):
        company_cared_id = cls.get_company_cared_id(dtu_id, dtu_type)
        rows = mysql.Find("info_company", "fire_authorities_id", {"id": company_cared_id})
        if len(rows)>0:
            return rows[0][0]
        else:
            return -1


    @classmethod
    def get_device_ids(cls, dtu_id):
        devices = []
        for row in mysql.Find("info_component", ["component_code"], {"dtu_id": dtu_id}) or []:
            dev = {"id":int(row[0]), "type":"device"}
            devices.append(dev)
        return devices


if __name__ == '__main__':
    print dtu().get_device_ids(113)
