from django.contrib import auth
from django.contrib.auth.models import User
from vividBtnAIO import utils


# Create your views here.


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
