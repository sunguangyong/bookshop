# -*- coding: utf-8 -*-

import pyutil.common.sys_utf8
from mako.template import Template
from mako.runtime import Context

from StringIO import StringIO
import os
import sys

config_module_name = ''
template_dir = ''
api_dir = ''
app_dir = ''


def check_output_api_dir():
    if not os.path.exists(api_dir):
        print "Warning, create output api dir=", api_dir
        os.mkdir(api_dir)

def gen_api(dbname, table_name, table_id, primary_keys):
    with open('%s/default.py'%(template_dir)) as f:
        t = Template(f.read())
        primary_keys_str = ", ".join(primary_keys)

        print "WHERE=", app_dir, "WHO=", table_name.capitalize(), "table_name=", table_name, "PRIMARY_KEYS=",primary_keys

        py_code = t.render(WHERE=app_dir, WHO=table_name.capitalize(), table_name=table_name, table_id=table_id, primary_keys=primary_keys, PRIMARY_KEYS_STR=primary_keys)
        print py_code

        of = open('%s/%s.py'%(api_dir, table_name), 'w')
        of.write(py_code)
        of.close()

def gen_init_py(dbname):
    path = '%s/__init__.py' % (api_dir)
    with open(path, 'w') as f: 
        f.write("# -*- coding: utf8 -*- ")

def gen_server(dbname, tables, module):
    
    tables_list = []
    for name in tables.keys():
        tables_list.append({'who':name.capitalize(), 'name':name, 'dbname':dbname, 'module':module})

    with open('%s/server.py'%(template_dir)) as f:
        t = Template(f.read())
        py_code = t.render(WHERE=app_dir, tables=tables_list)
        print py_code
        with open('%s/server.py'%(api_dir), 'w') as of: 
            of.write(py_code)

def main():
    print "config_module_name:", config_module_name
    config_module = __import__(config_module_name)
    print dir(config_module)
    modules = config_module_name.split(".")
    print modules
    for name in modules[1:]:
        config_module = getattr(config_module, name)
    tables = config_module.tables
    dbname = config_module.dbname

    check_output_api_dir()
    for table_name in tables.keys():
        if tables[table_name].get("manual"):
            continue  #不再自动生成戴安；手工实现
        primary_keys = tables[table_name].get("primary") or ["id"]
        table_id = tables[table_name].get("id") or "id"
        gen_api(dbname, table_name, table_id, primary_keys)

    gen_server(dbname, tables, api_dir.replace("/", " ").strip().replace(' ', '.'))
    gen_init_py(dbname)

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print "usage:\n python pyutil/dotage/gen_flask.py $CONFIG_PATH $INPUT_TEMPLATE_DIR $OUTPUT_API_DIR" 
        sys.exit(-1)
    config_module_name = sys.argv[1]
    template_dir = sys.argv[2]
    api_dir = sys.argv[3]
    app_dir = config_module_name.split(".")[0]
    main()
