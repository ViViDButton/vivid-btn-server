"""vividBtnAIO URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import re_path
from configparser import ConfigParser

from vividBtn import views as vbv
from AIO_auth import views as auth_v
from AIO_auth import permission

config = ConfigParser()
config.read('config/config.ini', encoding='UTF-8')

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^add-voice$', vbv.add_voice_data),
    re_path(r'^get-voice$', vbv.get_voice),
    re_path(r'^add-vtuber$', vbv.add_vtuber),
    re_path(r'^add-group$', vbv.add_group),
    re_path(r'^count$', vbv.item_click),
    re_path(r'^get-vtb$', vbv.get_vtb),
    re_path(r'^get-group$', vbv.get_group),
    re_path(r'^del-voice$', vbv.delete_voice),
    re_path(r'^del-group$', vbv.delete_group),
    re_path(r'^del-vtb$', vbv.delete_vtb),

    # 用户认证类
    re_path(r'^get-login-status$', auth_v.get_login_status),
    re_path(r'^user-login$', auth_v.user_login),
    re_path(r'^user-logout$', auth_v.user_logout),
    re_path(r'^list-user$', auth_v.list_user),
    re_path(r'^change-user-status$', auth_v.change_status),
    re_path(r'^delete-user$', auth_v.delete_user),
    re_path(r'^add-user$', auth_v.add_user),

    # 权限管理
    re_path(r'^get-group-list$', permission.get_group_list),
    re_path(r'^get-permission-list$', permission.get_permission_list),
]


if config['Common']['develop_mode'] == 'True':
    urlpatterns = urlpatterns + [
        # 请不要在生产环境打开本功能
        re_path(r'^admin$', admin.site.urls),
        re_path(r'^del-all$', vbv.del_all),
        re_path(r'^c-u$', auth_v.no_create_usr),
        re_path(r'^d-u$', auth_v.no_del_usr),
        re_path(r'^g-u$', auth_v.get_user),
        re_path(r'^l-u$', auth_v.login),
        re_path(r'^t-u$', auth_v.test),
        re_path(r'^t$', permission.set_group_permission),
    ]
