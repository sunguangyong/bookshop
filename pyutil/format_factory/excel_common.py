# coding=utf-8

"""
@author: Reggie
@time:   2018/08/03 14:28
@description:通用excel方法
"""

import xlwt
import xlsxwriter


def common_excel(data_map, out_file):
    """
    通用xls格式excel操作（兼容2003之后的）

    Args：
        data_map:   传入的数据
        out_file:   输出文件

    Return:
        out_file    输出文件路径
    """
    workbook = xlwt.Workbook()
    sheet1 = workbook.add_sheet(data_map.get(u'sheet_name', u"sheet1"))

    info = data_map.get('info', [])

    col_width = {}

    row = 0
    for li in info:
        for i in range(0, len(li)):

            if col_width.has_key(i):
                if len(unicode(li[i])) > col_width[i]:
                    col_width[i] = len(li[i])
            else:
                col_width[i] = len(li[i])

            sheet1.write(row, i, li[i], xlwt.easyxf(u'font: name 等线, height 220;align: wrap on, vert centre, horiz center'))
        row += 1

    for i in col_width.keys():
        if col_width[i] > 5:
            sheet1.col(i).width = 550 * (col_width[i] + 1)

    workbook.save(out_file)

    return out_file


def common_excel_xlsx(data_map, out_file):
    """
    通用xlsx格式Excel封装（兼容2007之后的）
    
    Args：
        data_map :   传入的数据
        out_file :   输出文件目录

    Return:
        out_file
    """

    workbook = xlsxwriter.Workbook(out_file, {'constant_memory': True})
    sheet = workbook.add_worksheet(data_map.get('sheet_name', 'sheet1'))

    v_center = workbook.add_format(
        {
            'valign': 'vcenter',
            'align': 'center',
            "bold": False,
            'font': u'等线',
            'size': 11,
            # 'bottom': 1,
            # 'right': 1,
            'text_wrap': 1,
        })

    info = data_map.get('info', [])

    col_width = {}

    row = 0
    for li in info:
        for i in range(0, len(li)):

            if col_width.has_key(i):
                if len(unicode(li[i])) > col_width[i]:
                    col_width[i] = len(li[i])
            else:
                col_width[i] = len(li[i])

            sheet.write(row, i, li[i], v_center)
        row += 1

    for i in col_width.keys():
        if col_width[i] > 5:
            sheet.set_column(i, i, 2 * (col_width[i] + 1))

    return out_file


def set_style(name, height, bold=False):
    """
    设置表格样式

    Args：
        name:   字体
        height: 字体强调
        bold:   字体加粗

    Return:
        nothing
    """
    style = xlwt.XFStyle()  # 初始化样式

    font = xlwt.Font()  # 为样式创建字体
    font.name = name  # 'Times New Roman'
    font.bold = bold
    font.color_index = 4
    font.height = height

    # borders= xlwt.Borders()
    # borders.left= 6
    # borders.right= 6
    # borders.top= 6
    # borders.bottom= 6

    style.font = font
    # style.borders = borders

    return style


if __name__ == '__main__':
    xlsx = 'demo1.xlsx'
    xls = 'demo2.xls'
    data_map = {"sheet_name": u"测试",
                "info": [
                    [u'业务', u'状态', u'北京', u'上海', u'广州', u'深圳', u'状态小计', u'合计'],
                    [u'业务业务业务', u'状态状态', u'北京北京北京', u'上海', u'广州', u'深圳', u'状态小计', u'合计'],
                    [u'业务业业务', u'状态状态状态', u'北京北北京', u'上海', u'广州', u'深圳', u'状态小计北京北京北京', u'合计'],
                    [u'业务业务业务业务', u'状态状态状态状态', u'北京北京北京', u'上海北京北京', u'广州', u'深圳', u'状态小计', u'合计'],
                    [u'业务业务业务', u'状态状态状态状态', u'北京北京北京京', u'上海', u'广州', u'深圳', u'状态小计', u'合计'],
                    [u'业务业务业务业务', u'状态状态状态状态', u'北京', u'上海', u'广州', u'深圳', u'状态小计', u'合计']
                ]}

    common_excel(data_map, xls)

    common_excel_xlsx(data_map, xlsx)
