# -*- coding: utf-8 -*-

import pyutil.common.sys_utf8
from mako.template import Template
from mako.runtime import Context
from pyutil.dotage.config_storage import tables
from pyutil.common.datetime_util import TimeNow 
from StringIO import StringIO
import os
import sys

template_dir = ''
output_dir = ''


def check_output_dir():
    if not os.path.exists(output_dir):
        print "Warning, create output code dir=", output_dir
        os.mkdir(output_dir)

def gen_storage(timestr, table_name, table_id):
    with open('%s/storage_template.py'%(template_dir)) as f:
        t = Template(f.read())

        print "time=", timestr, "table_name = ", table_name, "table_id = ", table_id
        py_code = t.render(TIME=timestr, table_name=table_name, table_id=table_id)
        print py_code

        of = open('%s/%s.py'%(output_dir, table_name), 'w')
        of.write(py_code)
        of.close()

def gen_init_py():
    path = '%s/__init__.py' % (output_dir)
    with open(path, 'w') as f: 
        f.write("# -*- coding: utf8 -*- ")

def main():
    check_output_dir()
    for table_name in tables.keys():
        if tables[table_name].get("manual"):
            continue  #不再自动生成戴安；手工实现
        table_id = tables[table_name].get("id") or "id"
        timestr = TimeNow()
        gen_storage(timestr, table_name, table_id)

    gen_init_py()

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print "usage:\n python pyutil/dotage/gen_storage.py  $INPUT_TEMPLATE_DIR $OUTPUT_DIR" 
        sys.exit(-1)
    template_dir = sys.argv[1]
    output_dir = sys.argv[2]
    main()
