# -*- coding: utf-8 -*- 

import pyutil.db.mellow as mellow
import pyconf.db.manna as manna


mysql = mellow.mellow(manna.config)

def main():
     
    water_cover = {"thing_id":31290890999, "thing_type":"info_device_dtu", "equipment_id":123981, "enum_device_class":10011, "enum_device_type":10008, "enum_device_model":10008, "enum_device_status":402}
    water_cover_index = {"thing_id":31290890999, "thing_type":"info_device_dtu"}

    water_press = {"thing_id":31290890888, "thing_type":"info_device_dtu", "equipment_id":123981, "enum_device_class":10011, "enum_device_type":10003, "enum_device_model":10003, "enum_device_status":206 }
    water_press_index = {"thing_id":31290890888, "thing_type":"info_device_dtu"}

    mysql.UpOrInsert("info_device", water_cover, water_cover_index)
    mysql.UpOrInsert("info_device", water_press, water_press_index)


    sense_1 = {"device_id":31290890999, "sense_type_id":2611}
    sense_2 = {"device_id":31290890888, "sense_type_id":2611}

    mysql.Insert("info_sense", sense_1)
    mysql.Insert("info_sense", sense_2)

    #mysql.Insert("info_device_dtu", record)


if __name__ == '__main__':
    main()
    


















if __name__ == '__main__':
    main()
