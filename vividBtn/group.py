from vividBtnAIO.utils import upyunAccount, response_json
from DataBaseModel.models import Voice, VoiceGroup, Vtuber
import json
import upyun

# TODO: 封装upyun上传文件的库

# 开源时务必删除账户信息
up = upyun.UpYun(upyunAccount['service'], upyunAccount['username'], upyunAccount['password'])
upyun_url = upyunAccount['upyun_url']
file_path = upyunAccount['file_path']


def get_group(request):
    vtb = request.GET.get('vtb-name')
    groups_list = VoiceGroup.objects.filter(vtb_name=vtb)
    group_list = []
    for group in groups_list:
        id = group.id
        name = group.group_name
        translate = group.translate
        click_count = group.all_count
        group_list.append({'id': id, 'name': name, 'translate': json.loads(translate), 'click_count': click_count})
    return response_json({'code': 200, 'vtb-name': vtb, 'groups': group_list})


def add_group(request):
    if request.method == 'GET':
        return response_json({'message': '请使用POST方法'}, 403)
    if not request.user.has_perm('DataBaseModel.add_group'):
        return response_json({'code': 403, 'message': '权限不足'})
    vtb_name = request.POST.get('vtb-name')
    group_name = request.POST.get('name')
    zh = request.POST.get('zh')
    ja = request.POST.get('ja')
    en = request.POST.get('en')
    translate = {'zh': zh, 'ja': ja, 'en': en}
    if not Vtuber.objects.filter(name=vtb_name):
        return response_json({'message': '没有此vtuber'}, 403)
    if VoiceGroup.objects.filter(vtb_name=vtb_name, group_name=group_name):
        return response_json({'message': '该分组已经存在'}, 403)
    group = VoiceGroup(vtb_name=vtb_name, group_name=group_name, all_count=0, translate=json.dumps(translate))
    group.save()
    return response_json({'message': '操作成功'})


def delete_group(request):
    if not request.user.has_perm('DataBaseModel.delete_group'):
        return response_json({'code': 403, 'message': '权限不足'})
    id = request.GET.get('id')
    group = VoiceGroup.objects.get(id=id)
    name = group.vtb_name
    group.delete()
    Voice.objects.filter(vtb_name=name).delete()
    return response_json({'code': 200, 'message': '删除成功'})


# 获取全部分组
def get_all_group(request):
    vtubers = Vtuber.objects.all()
    all_group_list = {}
    for vtuber in vtubers:
        name = vtuber.name
        groups = VoiceGroup.objects.filter(vtb_name=name)
        group_list = []
        for group in groups:
            group_list.append({
                'name': group.group_name,
                'id': group.id
            })
        all_group_list[name] = group_list
    return response_json({'code': 200, 'message': '操作成功', 'data': all_group_list})
