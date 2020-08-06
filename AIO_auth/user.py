from vividBtnAIO.utils import response_json
from django.contrib import auth
from django.contrib.auth.models import User, Group


# 检查登录状态---后台加载第一步
def get_login_status(request):
    if request.user.is_authenticated:
        return response_json({
            'code': 200,
            'message': '已登陆',
            'user': request.user.username,
            'first_name': request.user.first_name,
            'last_name': request.user.last_name
        })
    return response_json({'code': 403, 'message': '鉴权失败'})


# 登录
def user_login(request):
    if request.method == 'GET':
        return response_json({'code': 403, 'message': '请使用POST'})
    username = request.POST.get("username")
    password = request.POST.get("pwd")
    user_obj = auth.authenticate(username=username, password=password)
    auth.login(request, user_obj)
    return response_json({'user': 'user_obj.username'})


# 退出登录
def user_logout(request):
    auth.logout(request)
    return response_json({'message': '成功退出'})


# 列出用户 仅超管可用
def list_user(request):
    if not request.user.has_perm('auth.view_user'):
        return response_json({'code': 403, 'message': '权限不足'})
    all_user = User.objects.all()
    user_list = []
    for i in all_user:
        if i.is_superuser:
            group = '系统管理员'
        else:
            try:
                group = i.groups.all().first().name
            except:
                group = ''
        tmp = {
            'id': i.id,
            'name': i.username,
            'first_name': i.first_name,
            'last_name': i.last_name,
            'is_super': i.is_superuser,
            'group': group,
            'email': i.email,
            'is_active': i.is_active
        }
        user_list.append(tmp)
    return response_json({'code': 200, 'message': '操作成功', 'list': user_list})


# 更改用户状态
def change_status(request):
    if not request.user.has_perm('auth.change_user'):
        return response_json({'code': 403, 'message': '权限不足'})
    if request.POST.get('id'):
        id = int(request.POST.get('id'))
        user = User.objects.get(id=id)
        if len(User.objects.filter(is_superuser=True, is_active=True)) == 1 and user.is_superuser and user.is_active:
            return response_json({'code': 403, 'message': '您至少保留一个活动的超级管理员'})
        user.is_active = not user.is_active
        user.save()
        return response_json({'code': 200, 'message': '操作成功'})
    return response_json({'code': 403, 'message': '请写明参数'})


# 删除账户
def delete_user(request):
    if not request.user.has_perm('auth.delete_user'):
        return response_json({'code': 403, 'message': '权限不足'})
    if request.POST.get('id'):
        uid = int(request.POST.get('id'))
        user = User.objects.get(id=uid)
        if len(User.objects.filter(is_superuser=True, is_active=True)) == 1 and user.is_superuser:
            return response_json({'code': 403, 'message': '您至少保留一个活动的超级管理员'})
        user.delete()
        return response_json({'code': 200, 'message': '操作成功'})
    return response_json({'code': 403, 'message': 'ID错误'})


# 添加用户
def add_user(request):
    if not request.user.has_perm('auth.add_user'):
        return response_json({'code': 403, 'message': '权限不足'})
    try:
        user_name = request.POST.get('user_name')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('pwd')
        user_group = request.POST.get('group')
        User.objects.create_user(username=user_name, password=password, email=email)
        user = User.objects.get(username=user_name)
        user.first_name = first_name
        user.last_name = last_name
        user.groups.clear()
        user.groups.add(Group.objects.get(name=user_group))
        user.save()
    except Exception as e:
        return response_json({'code': 403, 'message': '解析参数失败'})
    return response_json({'code': 200, 'message': '操作成功'})


