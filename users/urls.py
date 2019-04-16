# coding:utf-8
from django.conf.urls import url
from users.views import register, register_handle, Test

urlpatterns = [
    url(r'^register/$', register, name="register"),
    url(r'^register_handle/$', register_handle, name='register_handle'),  # 用户注册处理
    url(r'^test/$', Test.as_view(), name='test'),  # 用户注册处理
]
