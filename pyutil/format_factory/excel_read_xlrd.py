# coding=utf-8

"""
@author: Reggie
@time:   2018/08/04 15:57
"""

import xlrd
import json
import sys

reload(sys)
sys.setdefaultencoding("utf-8")


def Print(s, indent=1, sort_keys=False):
    import json
    Utf8 = json.JSONEncoder(encoding='utf-8', ensure_ascii=False, indent=indent, sort_keys=sort_keys)
    print Utf8.encode(s)
    return Utf8.encode(s)


def read_excel(file_path, sheet_name='sheet1'):
    """
    将excel文件读取出来， 返回json格式的数据

    Args：
        file_path:   文件路径

    Return:
        {
            sheet1:[
                [row1],[row1],[row1],
            ],
            sheet2:[
                [row1],[row1],[row1],
            ]
        }
    """
    ret = {}
    workbook = xlrd.open_workbook(file_path)
    sheet_names = workbook.sheet_names()
    # Print(sheet_names)
    for sheet_name in sheet_names:
        ret[sheet_name] = []
        sheet = workbook.sheet_by_name(sheet_name)
        # print sheet.nrows, sheet.ncols, sheet.number
        row = 0

        while row < sheet.nrows:
            temp_li = sheet.row_values(row)
            ret[sheet_name].append(temp_li)
            row += 1

    return ret


def save_excel_data(file_path, sheet_name='sheet1'):
    """
    将excel文件读取出来， 保存到相应的文件中， 并返回json数据

    注：保存文件仅仅是为了观察数据结构
    
    Args：
        file_path:   文件路径
    
    Return:
        {
            sheet1:[
                [row1],[row1],[row1],
            ],
            sheet2:[
                [row1],[row1],[row1],
            ]
        }
    """
    ret = {}
    workbook = xlrd.open_workbook(file_path)
    sheet_names = workbook.sheet_names()
    # Print(sheet_names)
    for sheet_name in sheet_names:
        ret[sheet_name] = []
        sheet = workbook.sheet_by_name(sheet_name)
        # print sheet.nrows, sheet.ncols, sheet.number
        row = 0
        f = open('temp%s.json' % sheet_name, 'w+')
        try:
            while row < sheet.nrows:
                temp_li = sheet.row_values(row)
                ret[sheet_name].append(temp_li)
                # temp_li = filter(None, temp_li)
                # Print(temp_li, 4)
                if row == 0:
                    f.write('[')
                row += 1
                f.write(json.dumps(temp_li, ensure_ascii=False, indent=4))
                if row == sheet.nrows:
                    f.write(']')
                    continue
                f.write(',\n')
        except Exception as e:
            print e
            f.close()
        f.close()

    return ret


if __name__ == '__main__':
    ret = read_excel(u'template/temp.xlsx')
    Print(ret, indent=4)
