# coding=utf-8
import xlsxwriter

"""
@author: Reggie
@time:   2018/07/28
"""


class ExcelTemps:

    @classmethod
    def patrol_report(cls, out_file, data_map):
        """
        巡查报告Excel

        Args:
            out_file:  输出文件路径（绝对路径）
            data_map:  数据（数据格式按照例子， 关键字也必须相同）

        Return:
            out_file
        """
        # 创建Excel对象, 后面的配置可以减少内存使用
        workbook = xlsxwriter.Workbook(out_file, {'constant_memory': True})  # constant_memory 开启时， 一定要顺序写入
        worksheet = workbook.add_worksheet()  # 创建sheet

        try:

            center_title = workbook.add_format(  # 添加样式
                {'align': 'center',
                 "bold": True,
                 'font': u'等线',
                 'size': 24,
                 'border': 1,
                 'text_wrap': 1
                 })

            center_company = workbook.add_format(
                {'align': 'center',
                 "bold": False,
                 'font': u'等线',
                 'size': 11,
                 'border': 1,
                 'text_wrap': 1
                 })

            left_description = workbook.add_format(
                {
                    'align': 'vcentre',
                    "bold": False,
                    'font': u'等线',
                    'size': 11,
                    'border': 1,
                    'text_wrap': 1
                })

            v_center = workbook.add_format(
                {
                    'valign': 'vcenter',
                    'align': 'center',
                    "bold": False,
                    'font': u'等线',
                    'size': 11,
                    'border': 1,
                    'text_wrap': 1,
                })

            # worksheet.set_row(1, 50)  # 设置行高
            # worksheet.set_row(2, 20)
            # worksheet.set_row(3, 22)
            # worksheet.set_row(4, 22)
            # worksheet.set_row(5, 22)
            # worksheet.set_row(6, 22)
            # worksheet.set_row(7, 22)
            # worksheet.set_row(8, 40)
            # worksheet.set_row(9, 20)

            # worksheet.set_column('A:A', 4)  # 设置列宽
            # worksheet.set_column('B:B', 6)
            # worksheet.set_column('C:C', 6)
            # worksheet.set_column('E:E', 16)
            # worksheet.set_column('F:F', 16)
            # worksheet.set_column('G:G', 16)
            worksheet.set_column('A:A', 4)  # 设置列宽
            worksheet.set_column('B:B', 8)
            worksheet.set_column('C:C', 8)
            worksheet.set_column('E:E', 18)
            worksheet.set_column('F:F', 18)
            worksheet.set_column('G:G', 18)
            # worksheet.set_column('H:H', 8)

            worksheet.merge_range('A2:G2', u'%s' % data_map.get('title', ''), center_title)  # 合并表格

            worksheet.merge_range('A3:G3', u'%s' % data_map.get('company_name', ''), center_company)

            worksheet.merge_range('A4:G4', u'%s' % data_map.get('patrol', ''), left_description)

            worksheet.merge_range('A5:E5', u'%s' % data_map.get('patrol_date', ''), left_description)
            worksheet.merge_range('F5:G5', u'%s' % data_map.get('patrol_peoples', ''), left_description)

            worksheet.merge_range('A6:E6', u'%s' % data_map.get('patrol_port', ''), left_description)
            worksheet.merge_range('F6:G6', u'%s' % data_map.get('patrol_port_done', ''), left_description)

            worksheet.merge_range('A7:E7', u'%s' % data_map.get('size_up', ''), left_description)
            worksheet.merge_range('F7:G7', u'%s' % data_map.get('size_down', ''), left_description)

            worksheet.merge_range('A8:E8', u'%s' % data_map.get('gen_order', ''), left_description)
            worksheet.merge_range('F8:G8', u'%s' % data_map.get('detail_date', ''), left_description)

            worksheet.merge_range('A9:G9', u'%s' % data_map.get('info_title', ''), left_description)

            if data_map.has_key('info'):
                start_proid = 10

                for i in data_map.get('info', []):
                    worksheet.write("A%s" % start_proid, i.get('id', ''), v_center)
                    worksheet.write("B%s" % start_proid, i.get('serial_num', ''), v_center)
                    worksheet.write("C%s" % start_proid, i.get('position', ''), v_center)
                    worksheet.write("D%s" % start_proid, i.get('time', ''), v_center)
                    worksheet.write("E%s" % start_proid, i.get('size_up', ''), v_center)
                    worksheet.write("F%s" % start_proid, i.get('size_down', ''), v_center)
                    worksheet.write("G%s" % start_proid, i.get('mark', ''), v_center)

                    # access_bag = i.get('access_bag', '')
                    # if isinstance(access_bag, dict):
                    #     worksheet.write_url("H%s" % start_proid, access_bag.get('pic_url', ''), v_center,
                    #                     access_bag.get('pic_name', ''))
                    # elif isinstance(access_bag, basestring):
                    #     worksheet.write("H%s" % start_proid, access_bag, v_center)

                    start_proid += 1

        except Exception as e:
            print '>' * 50
            print "错误:\t", e
            print "函数名:\t", cls.__name__
            print '文件目录:\t', __file__
            print '>' * 50
            workbook.close()

        finally:
            workbook.close()

        return out_file

    @classmethod
    def patrol_nape(cls, out_file, data_map):
        """
        巡检报告巡查项

        Args:
            out_file:  输出文件路径（绝对路径）
            data_map:  数据（数据格式按照例子， 关键字也必须相同）

        Return:
            out_file
        """
        # 创建Excel对象, 后面的配置可以减少内存使用
        workbook = xlsxwriter.Workbook(out_file, {'constant_memory': True})
        worksheet = workbook.add_worksheet()

        try:
            center_title = workbook.add_format(
                {'valign': 'vcenter',
                 'align': 'center',
                 "bold": True,
                 'font': u'黑体',
                 'size': 24,
                 'top': 1,
                 'right': 1,
                 'bg_color': 'FFC000',
                 'text_wrap': 1
                 })
            line_two = workbook.add_format(
                {'align': 'left',
                 'valign': 'vcenter',
                 "bold": False,
                 'font': u'黑体',
                 'size': 9,
                 'top': 1,
                 'right': 1,
                 'bottom': 1,
                 'bg_color': 'FFC000',
                 'text_wrap': 1
                 }
            )
            center_info = workbook.add_format(
                {'align': 'center',
                 'valign': 'vcenter',
                 "bold": False,
                 'font': u'黑体',
                 'size': 10,
                 'top': 1,
                 'right': 1,
                 'bottom': 1,
                 'bg_color': 'FFC000',
                 'text_wrap': 1
                 }
            )
            v_center = workbook.add_format(  # 样式自动换行居中
                {
                    'valign': 'vcenter',
                    'align': 'center',
                    "bold": False,
                    'font': u'等线',
                    'size': 10,
                    'border': 1,
                    'text_wrap': 1,
                })

            worksheet.set_row(0, 50)  # 设置行高
            worksheet.set_row(1, 22)
            worksheet.set_row(2, 22)
            worksheet.set_row(3, 22)
            worksheet.set_row(4, 24)

            worksheet.set_column('A:A', 10)  # 设置列宽
            worksheet.set_column('B:B', 20)
            worksheet.set_column('C:C', 15)
            worksheet.set_column('D:D', 10)
            worksheet.set_column('E:E', 25)
            worksheet.set_column('F:F', 40)
            worksheet.set_column('G:G', 25)
            worksheet.set_column('H:H', 20)

            worksheet.merge_range('A1:H1', data_map.get('title', ''), center_title)  # 合并列
            worksheet.merge_range('A2:H2', data_map.get('foot_time', ''), line_two)
            worksheet.merge_range('A3:H3', data_map.get('import_time', ''), line_two)
            worksheet.merge_range('A4:H4', data_map.get('import_person', ''), line_two)

            if data_map.has_key('fields'):
                fields = data_map.get('fields', {})
                for k in fields.keys():
                    worksheet.write('%s5' % k, fields.get(k, ''), center_info)

            if data_map.has_key('info'):
                row = 6
                for info in data_map['info']:
                    length = len(info['usr_info'])

                    if length > 1:
                        A = 'A%s:A%s' % (row, row + length - 1)
                        B = 'B%s:B%s' % (row, row + length - 1)
                        print A, B
                        name = info.get('name', '')
                        post = info.get('post', '')
                        worksheet.merge_range(B, name, cell_format=v_center)
                        worksheet.merge_range(A, "fdasfdasfadsf", cell_format=v_center)
                    else:
                        worksheet.write('A%s' % row, info.get('name', ''), v_center)
                        worksheet.write('B%s' % row, info.get('post', ''), v_center)

                    # for usr_info in info['usr_info']:
                    #     for k in usr_info.keys():
                    #         print usr_info[k], row
                    #         if k == 'H':
                    #             print usr_info[k]
                    #             for pic_name, pic_url in usr_info[k].items():
                    #                 print worksheet.write_url('%s%s' % (k, row), url=pic_url, cell_format=center_info, string=pic_name)
                    #         else:
                    #             worksheet.write('%s%s' % (k, row), usr_info[k], v_center)
                    #     row += 1
                    row += 1

        except Exception as e:
            print '>' * 50
            print "错误:\t", e
            print "函数名:\t", cls.__name__
            print '文件目录:\t', __file__
            print '>' * 50
            workbook.close()

        finally:
            workbook.close()

        return out_file


def func_1():
    out_file = u'巡查报告.xlsx'
    data_map = {
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
                  'access_bag': {'pic_name': u'图1', 'pic_url': 'http://140.143.208.176'}},
                 {'serial_num': u'XC20180714354',
                  'id': '3',
                  'position': u'二层楼梯间前侧',
                  'time': '12:08:45',
                  'size_up': u'1、管道及阀门标识-消防供水设施；2、阀门-消防供水设施',
                  'size_down': u'1、室外消火栓；2、消防水喉',
                  'mark': u'标识清晰且正确；已生成工单',
                  'access_bag': {'pic_name': u'图1', 'pic_url': 'http://140.143.208.176'}},
                 {'serial_num': 'XC20180714354',
                  'id': '4',
                  'position': u'二层楼梯间前侧',
                  'time': '12:08:45',
                  'size_up': u'1、管道及阀门标识-消防供水设施；2、阀门-消防供水设施',
                  'size_down': u'1、室外消火栓；2、消防水喉',
                  'mark': u'标识清晰且正确；已生成工单',
                  'access_bag': {'pic_name': u'图1', 'pic_url': 'http://140.143.208.176'}},
                 {'serial_num': u'XC20180714354',
                  'id': '5',
                  'position': u'二层楼梯间前侧',
                  'time': '12:08:45',
                  'size_up': u'1、管道及阀门标识-消防供水设施；2、阀门-消防供水设施',
                  'size_down': u'1、室外消火栓；2、消防水喉',
                  'mark': u'标识清晰且正确；已生成工单',
                  'access_bag': {'pic_name': u'图1', 'pic_url': 'http://140.143.208.176'}},
                 ]
    }

    print ExcelTemps.patrol_report(out_file, data_map)


def func_2():
    out_file = u"巡查项.xlsx"
    data_map = {
        'title': u'足迹列表',
        'foot_time': u'足迹区间: 2018-06-27 至 2018-07-26',
        'import_time': u'导出时间: 2018-07-27 11:42:34',
        'import_person': u'导出人：李千秋',
        'fields': {'A': u'姓名',  # 对应下面info中的name
                   'B': u'岗位',  # 对应下面info中的post
                   'C': u'日期',
                   'D': u'时间',
                   'E': u'定位建筑名',
                   'F': u'建筑地址',
                   'G': u'备注',
                   'H': u'图片', },
        'info': [
            {'name': u'张三然',  # 对应上面fields中的 A
             'post': u'一般维保人员',  # 对应上面fields中的 B
             'usr_info': [{
                 'C': u'2018-07-04',  # 日期  # 跟上面的fields字段对应， 去掉name， post
                 'D': u'10:37:23',  # 时间
                 'E': u'三盛大厦',  # 定位建筑名
                 'F': u'北京市海淀区马连洼街道东北旺中路165号三盛大厦',  # 建筑地址
                 'G': u'今日完成三盛大厦维保任务',  # 备注
                 'H': {u'图片': "http://140.143.208.176/detail?id=95&kind=myexpand"},  # 图片URL
             }
             ]},
            {'name': u'ergou',
             'post': u'一般维保人员',
             'usr_info': [{
                 'C': u'2018-07-04',  # 日期  # 跟上面的fields字段对应， 去掉name， post
                 'D': u'10:37:23',  # 时间
                 'E': u'三盛大厦',  # 定位建筑名
                 'F': u'北京市海淀区马连洼街道东北旺中路165号三盛大厦',  # 建筑地址
                 'G': u'今日完成三盛大厦维保任务',  # 备注
                 'H': {u'图片': "http://140.143.208.176/detail?id=95&kind=myexpand"},  # 图片URL
             },
             ]},
            {'name': u'xixi',
             'post': u'二班维保人员',
             'usr_info': [
                 {
                     'C': u'2018-07-04',  # 日期  # 跟上面的fields字段对应， 去掉name， post
                     'D': u'10:37:23',  # 时间
                     'E': u'三盛大厦',  # 定位建筑名
                     'F': u'北京市海淀区马连洼街道东北旺中路165号三盛大厦',  # 建筑地址
                     'G': u'今日完成三盛大厦维保任务',  # 备注
                     'H': {u'图片1': "http://140.143.208.176/detail?id=95&kind=myexpand"},  # 图片URL
                 },
                 {
                     'C': u'2018-07-04',  # 日期  # 跟上面的fields字段对应， 去掉name， post
                     'D': u'10:37:23',  # 时间
                     'E': u'三盛大厦',  # 定位建筑名
                     'F': u'北京市海淀区马连洼街道东北旺中路165号三盛大厦',  # 建筑地址
                     'G': u'今日完成三盛大厦维保任务',  # 备注
                     'H': {u'图片2': "http://140.143.208.176/detail?id=95&kind=myexpand"},  # 图片URL
                 },
                 {
                     'C': u'2018-07-04',  # 日期  # 跟上面的fields字段对应， 去掉name， post
                     'D': u'10:37:23',  # 时间
                     'E': u'三盛大厦',  # 定位建筑名
                     'F': u'北京市海淀区马连洼街道东北旺中路165号三盛大厦',  # 建筑地址
                     'G': u'今日完成三盛大厦维保任务',  # 备注
                     'H': {u'图片3': "http://140.143.208.176/detail?id=95&kind=myexpand"},  # 图片URL
                 },
             ]},
        ],
    }
    print ExcelTemps.patrol_nape(out_file=out_file, data_map=data_map)


if __name__ == '__main__':
    func_1()
    func_2()
