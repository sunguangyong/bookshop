
import pyutil.common.sys_utf8 as sys_utf8
import pyutil.db.mellow as mellow
import pyconf.db.realtime_db as realtime_db

mysql = mellow.mellow(realtime_db.config)

class center:

    def get_info(self, id):
        row = mysql.Find("info_center", [], {"id": id}, out=dict)
        return row

    def get_company_ids(self):
        company_ids = []
        for row in self.mysql.Find("relation_company_center", ["company_id",], {"center_id": center_id}, out=list): 
            if not row[0]:
                continue
            company_ids.append(row[0])
        return company_ids

if __name__ == '__main__':
    print sys_utf8.Utf8(center().get_info(1101004))
