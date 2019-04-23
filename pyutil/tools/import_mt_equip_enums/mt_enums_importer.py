# -*- coding: utf-8 -*-
import pyutil.format_factory.excel_read_xlrd as excel_read_xlrd
import json
import pyutil.db.mellow as mellow

"""
维保系统主系统,子系统,设施,设施检查项,检查项问卷入库
"""
class equip_importer:
    @classmethod
    def assemble_mt_equips(cls, raw_data):
        enum_system_list = list()# 主系统类型
        enum_sub_system_list = list()# 子系统类型
        enum_equip_type_list = list()# 设施类型
        enum_equip_check_item_list = list()# 设施检查项类型

        system_index = 0# 系统id索引
        sub_system_index = 0# 子系统id索引
        equip_index = 0# 设施id索引
        equip_check_index = 0# 设施检查项id索引
        for item in raw_data:
            """主系统"""
            system_dict = dict()
            if item[0]:# 存在即是一个系统
                system_index = system_index + 1
                system_dict["id"] = system_index
                system_dict["system_name"] = item[0]
                enum_system_list.append(system_dict)
            else:# 不存在使用旧数据,为内部服务
                system_dict["id"] = system_index
                system_dict["system_name"] = enum_system_list[system_index-1]["system_name"]

            """子系统"""
            sub_system_dict = dict()
            if item[1]:# 存在即是一个子系统
                sub_system_index = sub_system_index + 1
                sub_system_dict["id"] = sub_system_index
                sub_system_dict["sub_system_name"] = item[1]
                sub_system_dict["enum_system_type"] = system_dict["id"]
                enum_sub_system_list.append(sub_system_dict)
            else:
                sub_system_dict["id"] = sub_system_index
                sub_system_dict["sub_system_name"] = enum_sub_system_list[sub_system_index-1]["sub_system_name"]
                sub_system_dict["enum_system_type"] = system_dict["id"]

            """设施"""
            equip_dict = dict()
            if item[2]:# 存在既是一个设施
                equip_index = equip_index + 1
                equip_dict["id"] = equip_index
                equip_dict["equip_name"] = item[2]
                equip_dict["enum_system_type"] = system_dict["id"]
                equip_dict["enum_sub_system_type"] = sub_system_dict["id"]
                enum_equip_type_list.append(equip_dict)
            else:
                equip_dict["id"] = equip_index
                equip_dict["equip_name"] = enum_equip_type_list[equip_index-1]["equip_name"]
                equip_dict["enum_system_type"] = system_dict["id"]
                equip_dict["enum_sub_system_type"] = sub_system_dict["id"]

            """设施检查项"""
            equip_check_dict = dict()
            equip_check_index = equip_check_index + 1
            equip_check_dict["id"] = equip_check_index
            equip_check_dict["enum_equip_type"] = equip_dict["id"]
            equip_check_dict["monthly_check_item"] = item[3]
            equip_check_dict["quarterly_check_item"] = item[4]
            equip_check_dict["yearly_check_item"] = item[5]
            equip_check_dict["check_explain"] = item[6]
            equip_check_dict["questionnaire"] = cls.check_item_converter(item[7])
            enum_equip_check_item_list.append(equip_check_dict)

        # excel_read_xlrd.Print(enum_system_list)
        # excel_read_xlrd.Print(enum_sub_system_list)
        # excel_read_xlrd.Print(enum_equip_type_list)
        # excel_read_xlrd.Print(enum_equip_check_item_list)
        return enum_system_list, enum_sub_system_list, enum_equip_type_list, enum_equip_check_item_list


    @classmethod
    def check_item_converter(cls, raw_str=str):
        question_list = [item.strip() for item in raw_str.strip().split("\n")]
        converted_list = list()
        for item in question_list:
            temp_dict = dict()
            if ":" in item:# 填空题
                temp_dict["type"] = u"text"
                temp_dict["user_ans"] = u""
                content_list = list()
                content_list.append(item.strip()[: len(item)-3])
                content_list.append(item.strip()[len(item)-3:])
                # print "text",json.dumps(content_list, ensure_ascii=False, encoding="utf-8")
                temp_dict["content"] = content_list[0]
                if content_list[1] == u"str":
                    temp_dict["user_ans_type"] = u"str"
                elif content_list[1] == u"num":
                    temp_dict["user_ans_type"] = u"num"
                else:
                    print u"i have error, my text is->" + item
                    return u"i have error"
            elif "-" in item and "/" in item:# 选择题
                # print item
                temp_dict["type"] = u"select"
                temp_dict["default"] = u"-1"
                content_list = [item.strip() for item in item.strip().split("-")]
                # print "select",json.dumps(content_list, ensure_ascii=False, encoding="utf-8")
                temp_dict["content"] = content_list[0]
                answer_list = [item.strip() for item in content_list[1].strip().split("/")]
                # print "select",json.dumps(answer_list, ensure_ascii=False, encoding="utf-8")
                # print answer_list
                temp_dict["content_pos"] = answer_list[0]
                temp_dict["content_neg"] = answer_list[1]
                temp_dict["right_ans"] = answer_list[0]
                temp_dict["user_ans"] = u""
            else:
                print u"error, the questionnaire in xls have wrong text and flat text is-> " + item
                return u"i have error"
            converted_list.append(temp_dict)
        converted_list_str = json.dumps(converted_list, ensure_ascii=False, encoding="utf-8")
        # print converted_list_str
        return converted_list_str

    @classmethod
    def insert_list(cls, mysql, table_name, enum_list):
        for item in enum_list:
            indexMap={"id": item["id"]}
            mysql.InsertOrNot(tabName=table_name, dataMap=item, indexMap=indexMap)




if __name__ == '__main__':
    ret = excel_read_xlrd.read_excel(u'/Users/gunther/Desktop/import_maint_equips.xls', sheet_name="Sheet1")
    # excel_read_xlrd.Print(ret["Sheet1"], indent=4)
    enum_system_list, enum_sub_system_list, enum_equip_type_list, enum_equip_check_item_list = equip_importer.assemble_mt_equips(ret["Sheet1"])
    db_config_local = {
        "host" : "127.0.0.1",
        "port" : 3306,
        "database" : "manna_maint",
        "user" : "root",
        "password" : "root",
        "charset" : "utf8",
    }

    db_config_dev = {
        "host" : "172.16.15.252",
        "port" : 3366,
        "database" : "manna_maint",
        "user" : "prod",
        "password" : "Fubang@#$123",
        "charset" : "utf8",
    }

    mysql = mellow.mellow(db_config_dev)
    equip_importer.insert_list(mysql, "enum_system_type", enum_system_list)
    equip_importer.insert_list(mysql, "enum_sub_system_type", enum_sub_system_list)
    equip_importer.insert_list(mysql, "enum_equip_type", enum_equip_type_list)
    equip_importer.insert_list(mysql, "enum_equip_check_item", enum_equip_check_item_list)
