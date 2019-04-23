#!/usr/local/bin/python
# -*- coding: utf8 -*-

import subprocess  

def run(shell_cmd):
    output = subprocess.Popen([shell_cmd], stdout=subprocess.PIPE, shell=True).communicate()
    lines = output[0].split("\n")
    return lines

if __name__ == '__main__':
    shell_cmd = 'python -m pyutil/db/tool/db_compare/realtime_shenyang'
    lines = run(shell_cmd)
    print  lines
