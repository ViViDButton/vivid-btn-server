from django.contrib import auth
from django.contrib.auth.models import User, Group, Permission
from vividBtnAIO.utils import response_json


# 获取用户组列表
def get_group_list(request):
    if not request.user.is_superuser:
        return response_json({'code': 403, 'message': '权限不足'})
    group_format_data = []
    for group in Group.objects.all():
        group_permission = []
        for permission in group.permissions.all():
            group_permission.append({
                'permission_id': permission.id,
                'permission_name': permission.name,
            })
        group_format_data.append({
            'group_id': group.id,
            'group_name': group.name,
            'permission': group_permission
        })
    return response_json({'code': 200, 'message': '操作成功', 'data': group_format_data})


# 获取权限列表
def get_permission_list(request):
    if not request.user.is_superuser:
        return response_json({'code': 403, 'message': '权限不足'})
    permission_data = []
    for permission in Permission.objects.all():
        permission_data.append({
            'permission_id': permission.id,
            'permission_name': permission.name
        })
    return response_json({'code': 200, 'message': '操作成功', 'data': permission_data})
