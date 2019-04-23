# coding=utf-8

"""
@author: Reggie
@time:   2018/07/31 11:28
"""
import os


def format_factory(file_path, out_pdf):
    """
    利用 linux 软件 soffice 将doc/docx/ppt/pptx/xls/xlsx转换为PDF

    Args:
        file_path: 需要转换的文件路径
        out_pdf:   输出文件路径（包括文件名和扩展名）

    Returns:
        out_pdf
    """
    if not os.path.exists(file_path):
        raise Exception('No file found！！')

    command = 'soffice --headless --convert-to pdf ' + file_path + ' --outdir ' + os.path.split(out_pdf)[0]
    os.system(command)
    return out_pdf
