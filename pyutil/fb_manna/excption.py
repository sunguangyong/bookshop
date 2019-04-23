#!/usr/bin/env python
#-*- coding: utf-8 -*-

class FB_Exception(Exception):
	def __init__(self,value):
		self._value = value
		self._error = ''

	def __str__(self):
		str = repr(self._value)
		if str:
			return self._error + ':' + str
		else:
			return self._error



"""""""""""""""""""""""""""""""""""""""""""""""""""
通用异常定义
"""""""""""""""""""""""""""""""""""""""""""""""""""

"""
输入错误
"""
class FB_InputError(FB_Exception):
	def __init__(self,*value_args):
		super(FB_InputError,self).__init__(":".join(value_args))
		self._error = 'InputError'


"""
内部错误
"""
class FB_InnerError(FB_Exception):
	def __init__(self,*value_args):
		super(FB_InnerError,self).__init__(":".join(value_args))
		self._error = 'InnerError'


"""
请求其他http服务器错误
"""
class FB_HttpRequestError(FB_Exception):
	def __init__(self,*value_args):
		super(FB_HttpRequestError,self).__init__(":".join(value_args))
		self._error = 'HttpRequestError'


"""
redis数据库错误
"""
class FB_RedisError(FB_Exception):
	def __init__(self,*value_args):
		super(FB_RedisError,self).__init__(":".join(value_args))
		self._error = 'RedisError'



"""""""""""""""""""""""""""""""""""""""""""""""""""
木星业务管理模块自定义异常
"""""""""""""""""""""""""""""""""""""""""""""""""""


"""
资源不存在
"""
class FB_ThingNotExistError(FB_Exception):
	def __init__(self,*value_args):
		super(FB_ThingNotExistError,self).__init__(":".join(value_args))
		self._error = 'ThingNotExistError'



"""
无此权限
"""
class FB_PrivilegeError(FB_Exception):
	def __init__(self,*value_args):
		super(FB_PrivilegeError,self).__init__(":".join(value_args))
		self._error = 'PrivilegeError'



if __name__ == '__main__':
	try:
		raise FB_PrivilegeError("main_func_name", "error")

	except Exception,e:
		print str(e)

