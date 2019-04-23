# coding=utf-8
import jinja2
import datetime
from docx.shared import Mm
from docxtpl import DocxTemplate, InlineImage
import os


class DocTemplate(object):
    """维保任务模板"""

    @classmethod
    def gen_file_by_temp(self, temp_path, data_map, file_type=None, out_path=None):
        """
        输入模板， 数据， 文件类型， 生成相应类型的文件

        Args:
            data_map:   参数 map
            out_path:   输出文件夹（包括文件名）
            temp_path:  模板路径 绝对路径(推荐)/相对路径
            file_type:  控制输出文件类型 PDF / DOC / DOCX
                        (默认为‘doc’. 不区分大小写)

        Returns；
            out_path.
        """

        if file_type:
            file_type = file_type.lower()
        else:
            file_type = 'doc'

        if file_type in ["doc", 'docx', 'pdf']:

            if not out_path:
                out_path = temp_path.split('.')[0]
            if file_type == "pdf":
                out_pdf = out_path
                out_path = out_path.split('.')[0] + '.' + 'doc'

            doc = DocxTemplate(temp_path)

            # 控制图片判断
            if data_map.has_key('pic_list'):
                for temp in data_map['pic_list']:
                    pic_name = temp.get('name', '')
                    pic_path = temp.get('path', '')
                    pic_width = temp.get('width', '')
                    pic_height = temp.get('height', '')

                    if not all([pic_name, pic_path, ]):
                        continue
                    if isinstance(pic_height, int or float):
                        pic_width = Mm(pic_width)
                    else:
                        pic_width = None
                    if isinstance(pic_width, int or float):
                        pic_height = Mm(pic_height)
                    else:
                        pic_height = None

                    data_map[pic_name] = InlineImage(doc, pic_path, width=pic_width, height=pic_height)

            # testing that it works also when autoescape has been forced to True
            jinja_env = jinja2.Environment(autoescape=True)

            doc.render(data_map, jinja_env)
            doc.save(out_path)
            if file_type == 'pdf':
                # 下面这种方式只适用于Windows
                # doc2pdf(out_path, out_pdf)
                # 调用soffice命令将word文档转换成pdf文档
                print '\n', '*-' * 50
                command = 'soffice --headless --convert-to pdf ' + out_path + ' --outdir ' + os.path.split(out_pdf)[0]
                result_out = os.system(command)
                print '\n', '*-' * 50
                # 转换成功，则返回转换后的pdf文件, 删除中间文件
                os.remove(out_path)
                return out_pdf

            return out_path


def func_1(tp):
    temp_path = "template/weibao.docx"  # 模板文件目录
    out_path = "./generated." + tp.lower()  # 输出文件名
    data_map = {'title': u"建 筑 消 防 设 施",  # 注意编码问题
                'pic_list': [{"name": "myimageratio", 'path': 'pic/erweima.png', "width": 30, "height": 30}],
                'month': True,
                'quarter': False,
                'year': False,
                'project_name': u'汇冠大厦',  # 项目名称
                'client_company': u'汇冠大厦股份有限公司',  # 委托单位
                'mechanism': u'久安维保施工有限公司',  # 维保机构
                'aptitude': u'消防设施维护保养检测一级',  # 维保单位级别
                'date': str(datetime.datetime.now().strftime('%Y年%m月%d日')).decode('utf-8'),  # 生成报告日期
                'local_name': u'九小场所',  # 场所名称
                'address': u'汇冠大厦',  # 地址
                'principal': u'大张伟',  # 责任人
                "phone_num": u'135****6666',  # 电话
                "service_num": u'135****6666',  # 服务电话
                "date_slip": u'2018年03月01日 — 2019年02月28日（合同期限）',  # 合同期限
                'building_info': {  # 维保建筑物概况
                    'total_area': u'15公顷',
                    'info': [u'综合楼：建筑面积10000平米；地上5层，8000平米；地下2层，2000平米；建筑高度24米。',
                             u'建筑名称：']},
                'important_location': [u'消防控制室设置位置： 一层', u'消防水箱设置位置： 屋顶  容量：XX m3', u'消防水池设置位置： 地下室 容量： XXX  m3'],
                # 重点部位
                'maintenance': [
                    [{'status': True, "data": u"消防供电配电"}, {'status': True, "data": u"火灾报警系统电气火灾监控系统"}],
                    [{'status': False, "data": u"消防供水设施消火栓灭火系统"}, {'status': True, "data": u"自动喷水灭火系统"}],
                    [{'status': True, "data": u"气体灭火系统"}, {'status': True, "data": u"泡沫灭火系统机械防烟系统"}],
                    [{'status': False, "data": u"机械排烟系统"}, {'status': True, "data": u"应急广播"}],
                    [{'status': False, "data": u"集中控制应急照明系统及疏散指示标志消防专用电话"}, {'status': True, "data": u"防火分隔"}],
                    [{'status': True, "data": u"消防电梯"}, {'status': True, "data": u"细水雾灭火系统干粉灭火系统"}],
                    [{'status': False, "data": u"灭火器"}, {'status': True, "data": u"主要消防设施标识"}],
                    [{'status': False, "data": u"其他消防设施："}, {}]],  # 维护保养项目范围 (注意： 不足两个的补充空字典)
                'idea': u'保养的很好',  # 维护保养单位意见
                'aurhorized': 'Reggie',  # 编制人
                'director': 'Reggie',  # 技术负责人
                'total_report': [{'id': 15, 'system': u'消防系统', 'case': u'不符合'},
                                 {'id': 16, 'system': u'气体灭火系统', 'case': u'不符合'},
                                 {'id': 17, 'system': u'消防应急广播', 'case': u'符合'},
                                 {'id': 18, 'system': u'消防电源', 'case': u'不符合'},
                                 {'id': 20, 'system': u'水浸系统', 'case': u'符合'},
                                 {'id': 20, 'system': u'火灾报警系统', 'case': u'符合'},
                                 {'id': 20, 'system': u'细水雾灭火系统干粉灭火系统',
                                  'case': u'符合'},
                                 {'id': 20, 'system': u'自动喷水灭火系统', 'case': u'符合'},
                                 {'id': 19, 'system': u'气体灭火系统', 'case': u'不符合'}, ],  # 建筑消防设施报告汇总表
                'systems': [
                    {'sys_name': u'气体灭火系统', 'sys_model': u'火灾系统', 'device_name': u'烟雾传感器', 'check': u'设施完好率',
                     'check_info': u'应急检查', 'real_info': u'敞亮', 'status': True, 'note': u'检查人王'},
                    {'sys_name': u'消防系统', 'sys_model': u'火灾系统', 'device_name': u'烟雾传感器', 'check': u'设施完好率',
                     'check_info': u'应急检查', 'real_info': u'敞亮', 'status': True, 'note': u'检查人王'},
                    {'sys_name': u'消防电源', 'sys_model': u'火灾系统', 'device_name': u'烟雾传感器', 'check': u'设施完好率',
                     'check_info': u'应急检查', 'real_info': u'敞亮', 'status': True, 'note': u'检查人王'},
                    {'sys_name': u'自动喷水灭火系统', 'sys_model': u'火灾系统', 'device_name': u'烟雾传感器', 'check': u'设施完好率',
                     'check_info': u'应急检查', 'real_info': u'敞亮', 'status': True, 'note': u'检查人王'},
                ]
                }
    d = DocTemplate()
    ret = d.gen_file_by_temp(temp_path, data_map, tp, out_path=out_path)
    print ret


def func_2(tp):
    temp_path = u"template/weibao2.docx"  # 模板文件目录
    out_path = u"./generated." + tp  # 输出文件名
    data_map = {
        u"client_company": u"测试001",
        u"year": False,
        u"idea": [
            u"机械排烟系统-机械排烟系统-排烟阀、电动排烟窗、电动挡烟垂壁、排烟防火阀:查看标识不清晰;检查标志处：树冠"
        ],
        u"month": True,
        u"aptitude": u"消防设施维护保养检测一级",
        u"service_num": u"15201512159",
        u"principal": u"杨会军",
        u"title": u"建 筑 消 防 设 施",
        u"mechanism": u"测试1322",
        u"systems": [
            {
                u"check_list": [
                    {
                        u"status": True,
                        u"notes": u"无",
                        u"check": u"1、自动启动、排烟防火阀联动停止功能",
                        u"real_info": u"（）联锁启动对应风机能;风机（）自动关闭能;打开的排烟阀具体位置：会馆大厦四层;关闭的排烟阀具体位置：百度",
                        u"check_info": u"打开排烟阀能正常联锁启动风机，关闭排烟防火阀，风机能自动关闭（拍照排烟风机控制箱面板和排烟风机整体照"
                    }
                ],
                u"sys_name": u"机械排烟系统",
                u"sys_model": u"机械排烟系统",
                u"device_name": u"排烟风机"
            },
            {
                u"check_list": [
                    {
                        u"status": True,
                        u"notes": u"无",
                        u"check": u"1、测试排烟阀、电动排烟窗手动/自动开启功能；测试启动应正常，且反馈信号正常",
                        u"real_info": u"开启（）释放正常;主机（）接收反馈信号能;测试的排烟阀具体位置：新浪",
                        u"check_info": u"通过手动启动排烟阀、电动排烟窗、电动挡烟垂壁，均能正常开启释放，反馈信号应正常。能正常通过手动启闭排"
                    },
                    {
                        u"status": False,
                        u"notes": u"无",
                        u"check": u"2、标识",
                        u"real_info": u"查看标识不清晰;检查标志处：树冠",
                        u"check_info": u"标识应清晰、明显"
                    }
                ],
                u"sys_name": u"机械排烟系统",
                u"sys_model": u"机械排烟系统",
                u"device_name": u"排烟阀、电动排烟窗、电动挡烟垂壁、排烟防火阀"
            }
        ],
        u"maintenance": [
            [
                {
                    u"status": True,
                    u"data": u"机械排烟系统"
                },
                {
                    u"status": False,
                    u"data": u"气体灭火系统"
                }
            ],
            [
                {
                    u"status": False,
                    u"data": u"消防供电配电"
                },
                {
                    u"status": False,
                    u"data": u"电气火灾监控系统"
                }
            ],
            [
                {
                    u"status": False,
                    u"data": u"机械加压送风系统"
                },
                {
                    u"status": False,
                    u"data": u"细水雾灭火系统"
                }
            ],
            [
                {
                    u"status": False,
                    u"data": u"应急照明和疏散指示系统"
                },
                {
                    u"status": False,
                    u"data": u"探火灭火装置"
                }
            ],
            [
                {
                    u"status": False,
                    u"data": u"干粉灭火系统"
                },
                {
                    u"status": False,
                    u"data": u"消防供水设施"
                }
            ],
            [
                {
                    u"status": False,
                    u"data": u"消火栓（自动灭火装置）灭火系统"
                },
                {
                    u"status": False,
                    u"data": u"应急广播系统"
                }
            ],
            [
                {
                    u"status": False,
                    u"data": u"灭火器"
                },
                {
                    u"status": False,
                    u"data": u"自动喷水灭火系统"
                }
            ],
            [
                {
                    u"status": False,
                    u"data": u"泡沫灭火系统"
                },
                {
                    u"status": False,
                    u"data": u"防火分隔"
                }
            ],
            [
                {
                    u"status": False,
                    u"data": u"消防专用电话"
                },
                {
                    u"status": False,
                    u"data": u"消防电梯"
                }
            ],
            [
                {
                    u"status": False,
                    u"data": u"水喷雾灭火系统"
                },
                {
                    u"status": False,
                    u"data": u"火灾报警系统"
                }
            ]
        ],
        u"total_report": [
            {
                u"case": u"不符合",
                u"system": u"机械排烟系统",
                u"id": 1
            }
        ],
        u"building_info": {
            u"info": [
                u"中国12: 建筑面积11.0平米; 地上1层, 0.0平米; 地下0层, 0.0平米; 建筑高度0.0米"
            ],
            u"total_area": 11
        },
        u"authorized": u"杨会军",
        u"project_name": u"测试合同01",
        u"phone_num": u"15201512159",
        u"date_slip": u"'2018年07月22日'-'2019年02月28日'(合同期限)",
        u"important_location": [
            u"消防控制室设置位置: 消防控制室位置, 消防水箱设置位置: 消防水箱位置, 容量: 2000m³, 消防水池设置位置: 消防水池位置, 容量: 200m³"
        ],
        u"director": u"杨会军",
        u"address": u"重庆市市辖区涪陵区敦仁街道办事处",
        u"date": u"2018年08月01日",
        u"local_name": u"测试合同01",
        u"quarter": False
    }
    d = DocTemplate()
    ret = d.gen_file_by_temp(temp_path, data_map, tp, out_path=out_path)
    print ret

def func_3(tp):
    temp_path = u"template/patrol_report.docx"  # 模板文件目录
    out_path = u"./generated." + tp  # 输出文件名
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
                  'access_bag': {'pic_name': u'图1', 'pic_url': u'http://140.143.208.176'}},
                 {'serial_num': u'XC20180714354',
                  'id': '3',
                  'position': u'二层楼梯间前侧',
                  'time': '12:08:45',
                  'size_up': u'1、管道及阀门标识-消防供水设施；2、阀门-消防供水设施',
                  'size_down': u'1、室外消火栓；2、消防水喉',
                  'mark': u'标识清晰且正确；已生成工单',
                  'access_bag': {'pic_name': u'图1', 'pic_url': u'http://140.143.208.176'}},
                 {'serial_num': 'XC20180714354',
                  'id': '4',
                  'position': u'二层楼梯间前侧',
                  'time': '12:08:45',
                  'size_up': u'1、管道及阀门标识-消防供水设施；2、阀门-消防供水设施',
                  'size_down': u'1、室外消火栓；2、消防水喉',
                  'mark': u'标识清晰且正确；已生成工单',
                  'access_bag': {'pic_name': u'图1', 'pic_url': u'http://140.143.208.176'}},
                 {'serial_num': u'XC20180714354',
                  'id': '5',
                  'position': u'二层楼梯间前侧',
                  'time': '12:08:45',
                  'size_up': u'1、管道及阀门标识-消防供水设施；2、阀门-消防供水设施',
                  'size_down': u'1、室外消火栓；2、消防水喉',
                  'mark': u'标识清晰且正确；\n已生成工单',
                  'access_bag': {'pic_name': u'图1', 'pic_url': u'http://140.143.208.176'}},
                 ]
    }
    d = DocTemplate()
    ret = d.gen_file_by_temp(temp_path, data_map, tp, out_path=out_path)
    print ret


if __name__ == '__main__':
    func_1('docx')
    func_1('doc')
    func_1('PDF')

    func_2('docx')
    func_2('doc')
    func_2('PDF')

    func_3('docx')
    func_3('doc')
    func_3('PDF')
