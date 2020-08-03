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

from vividBtn import group, voice, vtuber
from AIO_auth import permission, user
from vividBtnTranslate import translate

config = ConfigParser()
config.read('config/config.ini', encoding='UTF-8')

urlpatterns = [
    re_path(r'^add-voice$', voice.add_voice_data),
    re_path(r'^get-voice$', voice.get_voice),
    re_path(r'^add-vtuber$', vtuber.add_vtuber),
    re_path(r'^add-group$', group.add_group),
    re_path(r'^count$', vbv.item_click),
    re_path(r'^get-vtb$', vtuber.get_vtb),
    re_path(r'^get-group$', group.get_group),
    re_path(r'^del-voice$', voice.delete_voice),
    re_path(r'^del-group$', group.delete_group),
    re_path(r'^del-vtb$', vtuber.delete_vtb),
    re_path(r'^change-voice$', voice.change_voice),

    # 用户认证类
    re_path(r'^get-login-status$', user.get_login_status),
    re_path(r'^user-login$', user.user_login),
    re_path(r'^user-logout$', user.user_logout),
    re_path(r'^list-user$', user.list_user),
    re_path(r'^change-user-status$', user.change_status),
    re_path(r'^delete-user$', user.delete_user),
    re_path(r'^add-user$', user.add_user),

    # 权限管理
    re_path(r'^get-group-list$', permission.get_group_list),
    re_path(r'^get-permission-list$', permission.get_permission_list),
    re_path(r'^add-permission-group$', permission.add_permission_group),
    re_path(r'^delete-permission-group$', permission.del_permission_group),

    # 批量添加接口
    re_path(r'^get-default-voice$', voice.get_default_voice),
    re_path(r'^get-all-group$', group.get_all_group),

    # 翻译工作台接口
    re_path(r'^get-translate-list$', translate.get_translate_list),
    re_path(r'^submit-translate-log$', translate.submit_translate_log),
    re_path(r'^change-translate-status$', translate.change_status),
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
        re_path(r'^t$', voice.batch_upload),
    ]
