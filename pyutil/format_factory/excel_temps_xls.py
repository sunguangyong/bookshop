# coding=utf-8

"""
@author: Reggie
@time:   2018/08/03 16:48
"""
import copy

import xlwt


def set_style():
    style = xlwt.XFStyle()  # 初始化样式

    font = xlwt.Font()  # 为样式创建字体
    font.name = u"等线"  # 'Times New Roman'
    font.bold = True
    font.color_index = 4
    font.height = 550
    style.font = font

    borders = xlwt.Borders()
    borders.left = 1
    borders.right = 1
    borders.top = 1
    style.borders = borders

    alignment = xlwt.Alignment()
    alignment.horz = xlwt.Alignment.HORZ_CENTER  # 水平居中
    # alignment.vert = xlwt.Alignment.VERT_CENTER  # 垂直居中
    # alignment.wrap = xlwt.Alignment.WRAP_AT_RIGHT  # 自动换行
    style.alignment = alignment

    style.font = font
    # style.borders = borders

    return style


def patrol_report(data_map, out_file):
    """
    巡查报告模板

    Args：
        data_map:   数据
        out_file:   输出文件路径
            like:   /home/python/demo.xls

    Return:
        out_file:   输出文件路径
    """
    workbook = xlwt.Workbook()

    sheet1 = workbook.add_sheet(data_map.get('sheet_name', 'sheet1'))

    line7 = sheet1.col(6)
    line7.width = 256 * 20
    line6 = sheet1.col(5)
    line6.width = 256 * 20

    title_row_height = xlwt.easyxf('font:height 800')  # 20 * 36pt,类型小初的字号 18pt == 1
    row_height1 = xlwt.easyxf('font:height 350')

    style_title = xlwt.easyxf(
        u'font: name 等线, height 550, bold on ; align:wrap on, horiz center; borders: top 1, left 1, right 1')
    style_1 = xlwt.easyxf(
        u'font: name 宋体, height 216; align:wrap on, vert centre; borders: top 1, bottom 1, left 1, right 1')
    style_2 = xlwt.easyxf(
        u'font: name 宋体, height 216; align:wrap on, vert centre, horiz center; borders: bottom 1, left 1, right 1')

    row1 = sheet1.row(1)
    row1.set_style(title_row_height)

    for i in range(2, 9):
        row = sheet1.row(i)
        row.set_style(row_height1)

    # sheet1.col(0).width = 3333

    sheet1.write_merge(1, 1, 0, 6, data_map.get('title', ''), style_title)
    sheet1.write_merge(2, 2, 0, 6, data_map.get('company_name', ''), style_2)

    sheet1.write_merge(3, 3, 0, 6, data_map.get('patrol', ''), style_1)
    sheet1.write_merge(4, 4, 0, 4, data_map.get('patrol_date', ''), style_1)
    sheet1.write_merge(4, 4, 5, 6, data_map.get('patrol_peoples', ''), style_1)
    sheet1.write_merge(5, 5, 0, 4, data_map.get('patrol_port', ''), style_1)
    sheet1.write_merge(5, 5, 5, 6, data_map.get('patrol_port_done', ''), style_1)
    sheet1.write_merge(6, 6, 0, 4, data_map.get('size_up', ''), style_1)
    sheet1.write_merge(6, 6, 5, 6, data_map.get('size_down', ''), style_1)
    sheet1.write_merge(7, 7, 0, 4, data_map.get('gen_order', ''), style_1)
    sheet1.write_merge(7, 7, 5, 6, data_map.get('detail_date', ''), style_1)

    sheet1.write_merge(8, 8, 0, 6, data_map.get('info_title', ''), style_1)

    row = 9  # 上面格子最后一个格子加一
    if data_map.has_key('info'):
        for i in data_map.get('info', []):
            sheet1.write(row, 0, i.get('id', ''), style_1)
            sheet1.write(row, 1, i.get('serial_num', ''), style_1)
            sheet1.write(row, 2, i.get('position', ''), style_1)
            sheet1.write(row, 3, i.get('time', ''), style_1)
            sheet1.write(row, 4, i.get('size_up', ''), style_1)
            sheet1.write(row, 5, i.get('size_down', ''), style_1)
            sheet1.write(row, 6, i.get('mark', ''), style_1)
            # sheet1.write(row, col, i.get('access_bag', ''), style_1)
            row += 1

    workbook.save(out_file)

    return out_file


class PatrolNape(object):
    """
    人员足迹模板

    Args：
        sheet_name: sheet名,默认为`sheet1`
        data_map:   数据
        out_file:   输出文件路径
            like:   /home/python/demo.xls

    Return:
        out_file:   输出文件路径
    """

    def __init__(self, sheet_name='sheet1'):
        self.workbook = xlwt.Workbook()
        self.sheet = self.workbook.add_sheet(sheet_name)
        self.col_width = {}

        self.title_row_height = xlwt.easyxf('font:height 600')  # 20 * 36pt,类型小初的字号 18pt == 1
        self.comment_row_height = xlwt.easyxf('font:height 350')

        self.title_style = xlwt.easyxf(
            u'font: name 等线, height 400, bold on;\
             align:wrap on, horiz center, vert centre;\
              borders: top 1, left 1, right 1')
        self.comment_style = xlwt.easyxf(
            u'font: name 宋体, height 216;\
             align:wrap on, vert centre;\
              borders: top 1, bottom 1, left 1, right 1')
        self.comment_style_middle = xlwt.easyxf(
            u'font: name 宋体, height 216;\
             align:wrap on, vert centre, horiz center;\
              borders: bottom 1, left 1, right 1')
        self.url_style = xlwt.easyxf(
            u"font: name 等线, height 216, underline single, color blue;\
             align:wrap on, vert centre, horiz center;\
              borders: bottom 1, left 1, right 1;"
        )

    def add_col_width(self, k, v):
        """添加宽度列表"""
        if self.col_width.has_key(k):
            if self.col_width[k] < len(v):
                self.col_width[k] = len(v)
        else:
            self.col_width[k] = len(v)

    def auto_width(self):
        """自动宽度"""
        for i in range(len(self.col_width)):
            if i == 5:
                self.sheet.col(i).width = 256 * (self.col_width[i] + 25)
                continue
            elif i == 6:
                self.sheet.col(i).width = 256 * (self.col_width[i] + 20)
            elif self.col_width[i] > 4:
                self.sheet.col(i).width = 256 * (self.col_width[i] + 10)
            else:
                self.sheet.col(i).width = 256 * 10

    def deal_row_height(self, row_height_dic):
        """行高"""
        for row_range, row_height in row_height_dic.items():
            for row in range(row_range[0], row_range[1]):
                comment_row = self.sheet.row(row)
                comment_row.set_style(row_height)

    def deal_info(self, info, start_row):
        row = start_row
        temp_row = copy.copy(row)
        for i in info:
            length = len(i.get('usr_info', []))
            col_width_dic = {
                0: i.get('name', ''),
                1: i.get('position', ''),
            }
            temp_row = copy.copy(row)
            if length > 1:
                # comment_row = self.sheet.row(row)
                # comment_row.set_style(comment_row_height)
                for k, v in col_width_dic.items():
                    self.sheet.write_merge(row, row + length - 1, k, k, v, self.comment_style_middle)
                    self.add_col_width(k, v)
                row += length
            else:
                for k, v in col_width_dic.items():
                    self.sheet.write(row, k, v, self.comment_style_middle)
                    self.add_col_width(k, v)
                row += 1

            usr_info = i.get('usr_info', {})
            temp_row = self.deal_usr_info(usr_info, temp_row)

        return temp_row

    def deal_usr_info(self, usr_info, start_row):
        temp_row = start_row
        for usr_info in usr_info:
            col_width_dic = {
                2: usr_info.get('date', ''),
                3: usr_info.get('time', ''),
                4: usr_info.get('building_name', ''),
                5: usr_info.get('building_address', ''),
                6: usr_info.get('remark', ''),
                7: usr_info.get('picture', ''),
            }
            for k, v in col_width_dic.items():
                if k == 7:
                    self.sheet.write(temp_row, k, xlwt.Formula(u'HYPERLINK("%s";"图")' % v), self.url_style)
                    v = u"图片"
                else:
                    self.sheet.write(temp_row, k, v, self.comment_style_middle)
                self.add_col_width(k, v)
            temp_row += 1

        return temp_row

    def deal_fields(self, fields, start_row):
        row = start_row
        col_width_dic = {
            0: fields.get('name', ''),
            1: fields.get('position', ''),
            2: fields.get('date', ''),
            3: fields.get('time', ''),
            4: fields.get('building_name', ''),
            5: fields.get('building_address', ''),
            6: fields.get('remark', ''),
            7: fields.get('picture', ''),
        }
        for k, v in col_width_dic.items():
            self.sheet.write(row, k, v, self.comment_style_middle)
            self.add_col_width(k, v)

    def deal_title(self, data_map):
        col_width_dic = {
            0: data_map.get('title', ''),
            1: data_map.get('foot_time', ''),
            2: data_map.get('import_time', ''),
            3: data_map.get('import_person', ''),
        }
        for k, v in col_width_dic.items():
            if k == 0:
                self.sheet.write_merge(k, k, 0, 7, v, self.title_style)
            else:
                self.sheet.write_merge(k, k, 0, 7, v, self.comment_style)

    def run(self, data_map, out_file):
        """
        巡查项的模板

        Args：
            data_map:   数据
            out_file:   输出文件路径
                like:   /home/python/demo.xls

        Return:
            out_file:   输出文件路径
        """
        self.deal_title(data_map)

        fields = data_map.get('fields', {})
        self.deal_fields(fields, start_row=4)

        info = data_map.get('info', [])
        total_row = self.deal_info(info, start_row=5)

        row_height_dic = {
            (0, 1): self.title_row_height,
            (1, total_row): self.comment_row_height,
        }
        self.deal_row_height(row_height_dic)
        self.auto_width()
        self.workbook.save(out_file)

        return out_file


def func_1():
    out_file = u'巡查报告.xls'
    data_map = {
        'sheet_name': u'巡查报告',
        'title': u'巡查报告',
        'company_name': u'北京信息科技有限公司',
        'patrol': u'巡查描述',
        'patrol_date': u'巡查日期：2018年7月14日',
        'patrol_peoples': u'巡查人：张三、李四、王五等',
        'patrol_port': u'巡查点总数：45',
        'patrol_port_done': u'本次完成巡查点数：34',
        'size_up': u'符合数：30',
        'size_down': u'不符合数：4',
        'gen_order': u'生成工单数：2',
        'detail_date': u'生成报告时间：2018年7月14日  23:50:54',
        'info_title': u'巡查详情',
        'info': [{'id': u'序号',
                  'serial_num': u'巡查点编号',
                  'position': u'位置',
                  'time': u'巡查时间',
                  'size_up': u'符合巡查项',
                  'size_down': u'不符合巡查项',
                  'mark': u'记录',
                  'access_bag': u'附件'},
                 {'serial_num': 'XC20180714354',
                  'id': '2',
                  'position': u'二层楼梯间前侧',
                  'time': '12:08:45',
                  'size_up': u'1、管道及阀门标识-消防供水设施；2、阀门-消防供水设施',
                  'size_down': u'1、室外消火栓；2、消防水喉',
                  'mark': u'标识清晰且正确；已生成工单',
                  'access_bag': u'http://140.143.208.176'},
                 {'serial_num': u'XC20180714354',
                  'id': '3',
                  'position': u'二层楼梯间前侧',
                  'time': '12:08:45',
                  'size_up': u'1、管道及阀门标识-消防供水设施；2、阀门-消防供水设施',
                  'size_down': u'1、室外消火栓；2、消防水喉',
                  'mark': u'标识清晰且正确；已生成工单',
                  'access_bag': 'http://140.143.208.176'},
                 {'serial_num': 'XC20180714354',
                  'id': '4',
                  'position': u'二层楼梯间前侧',
                  'time': '12:08:45',
                  'size_up': u'1、管道及阀门标识-消防供水设施；2、阀门-消防供水设施',
                  'size_down': u'1、室外消火栓；2、消防水喉',
                  'mark': u'标识清晰且正确；已生成工单',
                  'access_bag': u'http://140.143.208.176'},
                 {'serial_num': u'XC20180714354',
                  'id': '5',
                  'position': u'二层楼梯间前侧',
                  'time': '12:08:45',
                  'size_up': u'1、管道及阀门标识-消防供水设施；2、阀门-消防供水设施',
                  'size_down': u'1、室外消火栓；2、消防水喉',
                  'mark': u'标识清晰且正确；\n已生成工单',
                  'access_bag': u'http://140.143.208.176'},
                 ]
    }
    print patrol_report(data_map, out_file)


def func_2():
    out_file = u'巡查项.xls'
    data_map = {
        'title': u'足迹列表',
        'foot_time': u'足迹区间: 2018-06-27 至 2018-07-26',
        'import_time': u'导出时间: 2018-07-27 11:42:34',
        'import_person': u'导出人：李千秋',
        'fields': {'name': u'姓名',  # 对应下面info中的name
                   'position': u'岗位',  # 对应下面info中的post
                   'date': u'日期',
                   'time': u'时间',
                   'building_name': u'定位建筑名',
                   'building_address': u'建筑地址',
                   'remark': u'备注',
                   'picture': u'图片', },
        'info': [
            {'name': u'张三然',  # 对应上面fields中的 A
             'position': u'一般维保人员',  # 对应上面fields中的 B
             'usr_info': [
                 {
                     'date': u'2018-07-04',  # 日期  # 跟上面的fields字段对应， 去掉name， post
                     'time': u'10:37:23',  # 时间
                     'building_name': u'三盛大厦',  # 定位建筑名
                     'building_address': u'北京市海淀区马连洼街道东北旺中路165号三盛大厦',  # 建筑地址
                     'remark': u'今日完成三盛大厦维保任务',  # 备注
                     'picture': "http://140.143.208.176/detail?id=95&kind=myexpand",  # 图片URL
                 },
             ]
             },
            {'name': u'张1然',  # 对应上面fields中的 A
             'position': u'一般维保人员',  # 对应上面fields中的 B
             'usr_info': [
                 {
                     'date': u'2018-07-04',  # 日期  # 跟上面的fields字段对应， 去掉name， post
                     'time': u'10:37:23',  # 时间
                     'building_name': u'三盛大厦',  # 定位建筑名
                     'building_address': u'北京市海淀区马连洼街道东北旺中路165号三盛大厦',  # 建筑地址
                     'remark': u'今日完成三盛大厦维保任务',  # 备注
                     'picture': "http://140.143.208.176/detail?id=95&kind=myexpand",  # 图片URL
                 },
             ]
             },
            {'name': u'jjj',
             'position': u'二班维保人员',
             'usr_info': [
                 {
                     'date': u'2018-07-04',  # 日期  # 跟上面的fields字段对应， 去掉name， post
                     'time': u'10:37:23',  # 时间
                     'building_name': u'三盛大厦',  # 定位建筑名
                     'building_address': u'北京市海淀区马连洼街道东北旺中路165号三盛大厦',  # 建筑地址
                     'remark': u'今日完成三盛大厦维保任务',  # 备注
                     'picture': "http://140.143.208.176/detail?id=95&kind=myexpand",  # 图片URL
                 },
                 {
                     'date': u'2018-07-04',  # 日期  # 跟上面的fields字段对应， 去掉name， post
                     'time': u'10:37:23',  # 时间
                     'building_name': u'三盛大厦',  # 定位建筑名
                     'building_address': u'北京市海淀区马连洼街道东北旺中路165号三盛大厦',  # 建筑地址
                     'remark': u'今日完成三盛大厦维保任务',  # 备注
                     'picture': "http://140.143.208.176/detail?id=95&kind=myexpand",  # 图片URL
                 },
                 {
                     'date': u'2018-07-04',  # 日期  # 跟上面的fields字段对应， 去掉name， post
                     'time': u'10:37:23',  # 时间
                     'building_name': u'三盛大厦',  # 定位建筑名
                     'building_address': u'北京市海淀区马连洼街道东北旺中路165号三盛大厦',  # 建筑地址
                     'remark': u'今日完成三盛大厦维保任务',  # 备注
                     'picture': "http://140.143.208.176/detail?id=95&kind=myexpand",  # 图片URL
                 },
                 {
                     'date': u'2018-07-04',  # 日期  # 跟上面的fields字段对应， 去掉name， post
                     'time': u'10:37:23',  # 时间
                     'building_name': u'三盛大厦',  # 定位建筑名
                     'building_address': u'北京市海淀区马连洼街道东北旺中路165号三盛大厦',  # 建筑地址
                     'remark': u'今日完成三盛大厦维保任务',  # 备注
                     'picture': "http://140.143.208.176/detail?id=95&kind=myexpand",  # 图片URL
                 }
             ]},
            {'name': u'zzz',
             'position': u'二班维保人员',
             'usr_info': [
                 {
                     'date': u'2018-07-04',  # 日期  # 跟上面的fields字段对应， 去掉name， post
                     'time': u'10:37:23',  # 时间
                     'building_name': u'三盛大厦',  # 定位建筑名
                     'building_address': u'北京市海淀区马连洼街道东北旺中路165号三盛大厦',  # 建筑地址
                     'remark': u'今日完成三盛大厦维保任务',  # 备注
                     'picture': "http://140.143.208.176/detail?id=95&kind=myexpand",  # 图片URL
                 },
                 {
                     'date': u'2018-07-04',  # 日期  # 跟上面的fields字段对应， 去掉name， post
                     'time': u'10:37:23',  # 时间
                     'building_name': u'三盛大厦',  # 定位建筑名
                     'building_address': u'北京市海淀区马连洼街道东北旺中路165号三盛大厦',  # 建筑地址
                     'remark': u'今日完成三盛大厦维保任务',  # 备注
                     'picture': "http://140.143.208.176/detail?id=95&kind=myexpand",  # 图片URL
                 },
                 {
                     'date': u'2018-07-04',  # 日期  # 跟上面的fields字段对应， 去掉name， post
                     'time': u'10:37:23',  # 时间
                     'building_name': u'三盛大厦',  # 定位建筑名
                     'building_address': u'北京市海淀区马连洼街道东北旺中路165号三盛大厦',  # 建筑地址
                     'remark': u'今日完成三盛大厦维保任务',  # 备注
                     'picture': "http://140.143.208.176/detail?id=95&kind=myexpand",  # 图片URL
                 },
                 {
                     'date': u'2018-07-04',  # 日期  # 跟上面的fields字段对应， 去掉name， post
                     'time': u'10:37:23',  # 时间
                     'building_name': u'三盛大厦',  # 定位建筑名
                     'building_address': u'北京市海淀区马连洼街道东北旺中路165号三盛大厦',  # 建筑地址
                     'remark': u'今日完成三盛大厦维保任务',  # 备注
                     'picture': "http://140.143.208.176/detail?id=95&kind=myexpand",  # 图片URL
                 }
             ]},
            {'name': u'zzz',
             'position': u'二班维保人员',
             'usr_info': [
                 {
                     'date': u'2018-07-04',  # 日期  # 跟上面的fields字段对应， 去掉name， post
                     'time': u'10:37:23',  # 时间
                     'building_name': u'三盛大厦',  # 定位建筑名
                     'building_address': u'北京市海淀区马连洼街道东北旺中路165号三盛大厦',  # 建筑地址
                     'remark': u'今日完成三盛大厦维保任务',  # 备注
                     'picture': "http://140.143.208.176/detail?id=95&kind=myexpand",  # 图片URL
                 },
                 {
                     'date': u'2018-07-04',  # 日期  # 跟上面的fields字段对应， 去掉name， post
                     'time': u'10:37:23',  # 时间
                     'building_name': u'三盛大厦',  # 定位建筑名
                     'building_address': u'北京市海淀区马连洼街道东北旺中路165号三盛大厦',  # 建筑地址
                     'remark': u'今日完成三盛大厦维保任务',  # 备注
                     'picture': "http://140.143.208.176/detail?id=95&kind=myexpand",  # 图片URL
                 },
                 {
                     'date': u'2018-07-04',  # 日期  # 跟上面的fields字段对应， 去掉name， post
                     'time': u'10:37:23',  # 时间
                     'building_name': u'三盛大厦',  # 定位建筑名
                     'building_address': u'北京市海淀区马连洼街道东北旺中路165号三盛大厦',  # 建筑地址
                     'remark': u'今日完成三盛大厦维保任务',  # 备注
                     'picture': "http://140.143.208.176/detail?id=95&kind=myexpand",  # 图片URL
                 },
                 {
                     'date': u'2018-07-04',  # 日期  # 跟上面的fields字段对应， 去掉name， post
                     'time': u'10:37:23',  # 时间
                     'building_name': u'三盛大厦',  # 定位建筑名
                     'building_address': u'北京市海淀区马连洼街道东北旺中路165号三盛大厦',  # 建筑地址
                     'remark': u'今日完成三盛大厦维保任务',  # 备注
                     'picture': "http://140.143.208.176/detail?id=95&kind=myexpand",  # 图片URL
                 }
             ]},

            {'name': u'张1然',  # 对应上面fields中的 A
             'position': u'一般维保人员',  # 对应上面fields中的 B
             'usr_info': [
                 {
                     'date': u'2018-07-04',  # 日期  # 跟上面的fields字段对应， 去掉name， post
                     'time': u'10:37:23',  # 时间
                     'building_name': u'三盛大厦',  # 定位建筑名
                     'building_address': u'北京市海淀区马连洼街道东北旺中路165号三盛大厦',  # 建筑地址
                     'remark': u'今日完成三盛大厦维保任务',  # 备注
                     'picture': "http://140.143.208.176/detail?id=95&kind=myexpand",  # 图片URL
                 },
             ]
             },

            {'name': u'zzz',
             'position': u'二班维保人员',
             'usr_info': [
                 {
                     'date': u'2018-07-04',  # 日期  # 跟上面的fields字段对应， 去掉name， post
                     'time': u'10:37:23',  # 时间
                     'building_name': u'三盛大厦',  # 定位建筑名
                     'building_address': u'北京市海淀区马连洼街道东北旺中路165号三盛大厦',  # 建筑地址
                     'remark': u'今日完成三盛大厦维保任务',  # 备注
                     'picture': "http://140.143.208.176/detail?id=95&kind=myexpand",  # 图片URL
                 },
                 {
                     'date': u'2018-07-04',  # 日期  # 跟上面的fields字段对应， 去掉name， post
                     'time': u'10:37:23',  # 时间
                     'building_name': u'三盛大厦',  # 定位建筑名
                     'building_address': u'北京市海淀区马连洼街道东北旺中路165号三盛大厦',  # 建筑地址
                     'remark': u'今日完成三盛大厦维保任务',  # 备注
                     'picture': "http://140.143.208.176/detail?id=95&kind=myexpand",  # 图片URL
                 },
                 {
                     'date': u'2018-07-04',  # 日期  # 跟上面的fields字段对应， 去掉name， post
                     'time': u'10:37:23',  # 时间
                     'building_name': u'三盛大厦',  # 定位建筑名
                     'building_address': u'北京市海淀区马连洼街道东北旺中路165号三盛大厦',  # 建筑地址
                     'remark': u'今日完成三盛大厦维保任务',  # 备注
                     'picture': "http://140.143.208.176/detail?id=95&kind=myexpand",  # 图片URL
                 },
                 {
                     'date': u'2018-07-04',  # 日期  # 跟上面的fields字段对应， 去掉name， post
                     'time': u'10:37:23',  # 时间
                     'building_name': u'三盛大厦',  # 定位建筑名
                     'building_address': u'北京市海淀区马连洼街道东北旺中路165号三盛大厦',  # 建筑地址
                     'remark': u'今日完成三盛大厦维保任务',  # 备注
                     'picture': "http://140.143.208.176/detail?id=95&kind=myexpand",  # 图片URL
                 }
             ]},
        ],
    }
    patrol_nape = PatrolNape()
    print patrol_nape.run(data_map, out_file)


if __name__ == '__main__':
    # func_1()
    func_2()
