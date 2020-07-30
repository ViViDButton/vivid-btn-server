from django.contrib import auth
from django.contrib.auth.models import User
from vividBtnAIO import utils


# Create your views here.


# 检查登录状态---后台加载第一步
def get_login_status(request):
    if request.user.is_authenticated:
        return utils.response_json({
            'code': 200,
            'message': '已登陆',
            'user': request.user.username,
            'first_name': request.user.first_name,
            'last_name': request.user.last_name
        })
    return utils.response_json({'code': 403, 'message': '鉴权失败'})


# 登录
def user_login(request):
    if request.method == 'GET':
        return utils.response_json({'code': 403, 'message': '请使用POST'})
    username = request.POST.get("username")
    password = request.POST.get("pwd")
    user_obj = auth.authenticate(username=username, password=password)
    auth.login(request, user_obj)
    return utils.response_json({'user': 'user_obj.username'})


# 退出登录
def user_logout(request):
    auth.logout(request)
    return utils.response_json({'message': '成功退出'})


# 列出用户 仅超管可用
def list_user(request):
    if not request.user.is_superuser:
        return utils.response_json({'code': 403, 'message': '权限不足'})
    all_user = User.objects.all()
    user_list = []
    for i in all_user:
        tmp = {
            'id': i.id,
            'name': i.username,
            'first_name': i.first_name,
            'last_name': i.last_name,
            'is_super': i.is_superuser,
            'email': i.email,
            'is_active': i.is_active
        }
        user_list.append(tmp)
    return utils.response_json({'code': 200, 'message': '操作成功', 'list': user_list})


# 更改用户状态
def change_status(request):
    if not request.user.is_superuser and request.method == 'POST':
        return utils.response_json({'code': 403, 'message': '权限不足'})
    if request.POST.get('id'):
        id = int(request.POST.get('id'))
        user = User.objects.get(id=id)
        if len(User.objects.filter(is_superuser=True, is_active=True)) == 1 and user.is_superuser and user.is_active:
            return utils.response_json({'code': 403, 'message': '您至少保留一个活动的超级管理员'})
        user.is_active = not user.is_active
        user.save()
        return utils.response_json({'code': 200, 'message': '操作成功'})
    return utils.response_json({'code': 403, 'message': '请写明参数'})


# 删除账户
def delete_user(request):
    if not request.user.is_superuser:
        return utils.response_json({'code': 403, 'message': '权限不足'})
    if request.POST.get('id'):
        uid = int(request.POST.get('id'))
        user = User.objects.get(id=uid)
        if len(User.objects.filter(is_superuser=True, is_active=True)) == 1 and user.is_superuser:
            return utils.response_json({'code': 403, 'message': '您至少保留一个活动的超级管理员'})
        user.delete()
        return utils.response_json({'code': 200, 'message': '操作成功'})
    return utils.response_json({'code': 403, 'message': 'ID错误'})


# 添加用户
def add_user(request):
    if not request.user.is_superuser:
        return utils.response_json({'code': 403, 'message': '权限不足'})
    try:
        user_name = request.POST.get('user_name')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('pwd')
        is_super = request.POST.get('super')
        if is_super != 'true':
            User.objects.create_user(username=user_name, password=password, email=email)
        else:
            User.objects.create_superuser(username=user_name, password=password, email=email)
        user = User.objects.get(username=user_name)
        user.first_name = first_name
        user.last_name = last_name
        user.save()
    except Exception as e:
        return utils.response_json({'code': 403, 'message': '解析参数失败'})
    return utils.response_json({'code': 200, 'message': '操作成功'})


# 无权限创建管理员，禁止用于生产环境
def no_create_usr(request):
    usr = request.GET.get('usr')
    pwd = request.GET.get('pwd')
    isSuper = request.GET.get('super')
    if not isSuper:
        User.objects.create_user(username=usr, password=pwd)
        return utils.response_json({'message': 'success'})
    User.objects.create_superuser(username=usr, password=pwd, email='defa@dd.com')
    return utils.response_json({'message': 'success'})


def get_user(request):
    print(request.user.is_authenticated)
    print(request.user.is_superuser)
    print(request.user)
    return utils.response_json({'name': ''})


def login(request):
    username = request.GET.get("username")
    password = request.GET.get("pwd")
    user_obj = auth.authenticate(username=username, password=password)
    print(username, password, user_obj)
    auth.login(request, user_obj)
    return utils.response_json({'user': user_obj.username})


def no_del_usr(request):
    id = int(request.POST.get('id'))
    User.objects.get(id=id).delete()
    return utils.response_json({'message': '操作成功'})


def test(request):
    u = User.objects.create_user(username='user_name1', password='password', email='email')
    print(u.username)
    return utils.response_json({'message': '操作成功'})
