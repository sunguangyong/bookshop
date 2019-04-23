#!/usr/bin/env python
# -*- coding: utf-8 -*-

import functools
import pyutil.common.sys_utf8 as sys_utf8
from pyutil.fb_django.fb_views import GeneralView


def required_parameters(*parameters_list, **parameters_dict):
    def _decorater(func):
        @functools.wraps(func)
        def _wrapped_func(general_view, *args, **kwargs):

            parameters_4_check = []
            parameters_4_parse = []

            for field in parameters_list:
                items = [f.strip() for f in field.split(":")]
                if len(items)==1:
                    parameters_4_check.append(items[0])
                elif len(items)==2:
                    parameters_4_check.append("%s:%s" %(items[0], items[1]))
                    parameters_4_parse.append((items[0], items[1])) 
                else:
                    continue

            result = general_view.check_query( parameters_4_check )
            if result is not None:
                return general_view.send_error(*result)

            result = general_view.check_post( parameters_dict )
            if result is not None:
                return general_view.send_error(*result)

            def install_attr_view(general_view, parameters_4_parse):
                for param in parameters_4_parse:
                    if not general_view.url_params.get(param[1]):
                        continue
                    general_view[param[1]] = general_view.url_params.get(param[1])
                    if param[0]=='int':
                        general_view[param[1]] = int(general_view[param[1]])
                    elif param[0]=='float':
                        general_view[param[1]] = float(general_view[param[1]])

            install_attr_view(general_view, parameters_4_parse)

            free_parameters = [("int", "page_no"), ("int", "page_size")]
            install_attr_view(general_view, free_parameters)
     
            for param in free_parameters:
                if param[1] in general_view.url_params:
                    general_view[param[1]] = general_view.url_params[param[1]]

            return func(general_view, *args, **kwargs)
        return _wrapped_func
    return _decorater
