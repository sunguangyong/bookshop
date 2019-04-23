# -*- coding: utf-8 -*- 


def gen_component_id(dtu_id, alarm_host_no, loop_number=0, component_number=0, component_code=0):
    loop_number, component_number, component_code = int(loop_number or 0), int(component_number or 0), int(component_code or 0)
    if loop_number < 0:
        loop_number = 0
    if component_number < 0:
        component_number = 0
    if component_code < 0:
        component_code = 0

    if loop_number>0 or component_number>0:
        component_code= "%3d%03d" % (loop_number%1000, component_number%1000)
    component_code = str(component_code)[-6:]

    component_id = "%s%06d%03d" % (str(dtu_id)[-8:], int(component_code), int(str(alarm_host_no)[-3:]))
    return int(component_id)

def gen_alarmer_id(dtu_id, alarm_host_no):
    alarmer_id = "%s%03d" % (str(dtu_id)[-15:], int(str(alarm_host_no)[-3:]))
    return int(alarmer_id)


if __name__ == '__main__':
    dtu_id = 356566070718614
    alarm_host_no = 0
    loop_number = 59
    component_number =  1299
    print gen_component_id(dtu_id, alarm_host_no, loop_number, component_number)
