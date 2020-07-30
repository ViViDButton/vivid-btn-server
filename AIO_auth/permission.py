from django.contrib import auth
from django.contrib.auth.models import User, Group, Permission
from vividBtnAIO.utils import response_json


# 获取用户组列表
def get_group_list(request):
    if not request.user.has_perm('auth.view_group'):
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
    if not request.user.has_perm('auth.view_permission'):
        return response_json({'code': 403, 'message': '权限不足'})
    permission_data = []
    for permission in Permission.objects.all():
        permission_data.append({
            'permission_id': permission.id,
            'permission_name': permission.name
        })
    return response_json({'code': 200, 'message': '操作成功', 'data': permission_data})


# 添加用户到权限组
def add_user_to_group(request):
    pass


# 权限组设置
def set_group_permission(request):
    if not request.user.has_perm('auth.change_group'):
        return response_json({'code': 403, 'message': '权限不足'})
    if not request.method == 'POST':
        return response_json({'code': 403, 'message': '该请求只适用于POST方法'})
    permission_list = request.POST.get('permission')
    group_name = request.POST.get('group')
    permission_list = permission_list.replace('[', '').replace(']', '').replace('\'', '').split(',')
    permission_list_obj = []
    for permission in permission_list:
        permission_list_obj.append(Permission.objects.get(name=permission.lstrip().rstrip()))
    Group.objects.get(name=group_name).permissions.set(permission_list_obj)
    return response_json({'code': 200})
