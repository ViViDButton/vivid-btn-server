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
            'permission_name': permission.name,
            'permission_codename': permission.codename
        })
    return response_json({'code': 200, 'message': '操作成功', 'data': permission_data})


# 添加用户到权限组
def add_user_to_group(request):
    pass


# 格式化权限
def format_permission(permission_list):
    permission_list = permission_list.replace('[', '').replace(']', '').replace('\'', '').split(',')
    permission_list_obj = []
    for permission in permission_list:
        permission_list_obj.append(Permission.objects.get(id=permission))
    return permission_list_obj


# 用户组设置
def set_group_permission(request):
    if not request.user.has_perm('auth.change_group'):
        return response_json({'code': 403, 'message': '权限不足'})
    if not request.method == 'POST':
        return response_json({'code': 403, 'message': '该请求只适用于POST方法'})
    group_name = request.POST.get('group')
    permission_list_obj = format_permission(request.POST.get('permission'))
    Group.objects.get(name=group_name).permissions.set(permission_list_obj)
    return response_json({'code': 200})


# 添加用户组
def add_permission_group(request):
    if not request.user.has_perm('auth.add_group'):
        return response_json({'code': 403, 'message': '权限不足'})
    permission_list = format_permission(request.POST.get('permission'))
    group = Group.objects.create(name=request.POST.get('name'))
    group.permissions.set(permission_list)
    group.save()
    return response_json({'code': 200, 'message': '操作成功'})


# 删除用户组
def del_permission_group(request):
    if not request.user.has_perm('auth.delete_group'):
        return response_json({'code': 403, 'message': '权限不足'})
    gid = request.POST.get('id')
    Group.objects.get(id=gid).delete()
    return response_json({'code': 200, 'message': '操作成功'})

