from vividBtnAIO.utils import upyunAccount, response_json, handle_pic_upload
from vividBtnTranslate import translate
from DataBaseModel.models import Voice, VoiceGroup, Vtuber
import json
import upyun

# TODO: 封装upyun上传文件的库

# 开源时务必删除账户信息
up = upyun.UpYun(upyunAccount['service'], upyunAccount['username'], upyunAccount['password'])
upyun_url = upyunAccount['upyun_url']
file_path = upyunAccount['file_path']


# Utils
# 版本控制
def version_control(vtb, next_ver):
    if next_ver == '1':
        try:
            prew_ver_voice = Voice.objects.filter(vtb_name=vtb, tag='new')
            for item in prew_ver_voice:
                item.tag = ''
                item.save()
            return True
        except:
            print('更改失败')
            return False
    return True


# API
def add_voice_data(request):
    if request.method == 'GET':
        return response_json({'message': '请使用POST方法'}, 403)
    if not request.user.has_perm('DataBaseModel.add_voice'):
        return response_json({'code': 403, 'message': '权限不足'})
    vtb_name = request.POST.get('vtb-name')
    name = request.POST.get('voice-name')
    group = request.POST.get('group-name')
    file_obj = request.FILES.get('file')

    # 版本控制
    if request.POST.get('next_ver'):
        version_control(vtb_name, request.POST.get('next_ver'))

    url = handle_pic_upload(file_obj, vtb_name)

    if url['code'] == 403:
        return response_json(url)

    url = url['url']

    version = request.POST.get('ver')
    count = 0

    translate.add_translate(request, name, 'voice')

    # 检查是否有本vtb
    if not Vtuber.objects.filter(name=vtb_name):
        return response_json({'message': '请先创建此vtuber'}, 403)
    if not VoiceGroup.objects.filter(group_name=group):
        return response_json({'message': '没有此分组!'}, 403)
    voice = Voice(vtb_name=vtb_name, name=name, group=group, url=url, version=version, count=count
                  , translate='', tag='new')
    voice.save()
    return response_json({'message': '操作成功', 'file_locate': url})


# 批量上传
def batch_upload(request):
    if not request.user.has_perm('DataBaseModel.add_voice'):
        return response_json({'code': 403, 'message': '权限不足'})
    if request.POST.get('vtuber') != '':
        vtb_name = request.POST.get('vtuber')
    else:
        vtb_name = 'default'
    upload_resp = handle_pic_upload(request.FILES.get('file'), vtb_name)
    name = upload_resp['file_name']
    url = upload_resp['url']

    translate.add_translate(request, name, 'voice')

    voice = Voice(vtb_name=vtb_name, name=name, group='default', url=url, count=0, tag='new')
    voice.save()

    return response_json({'code': 200})


# 查询default分组
def get_default_voice(request):
    if request.GET.get('vtb'):
        vtb = request.GET.get('vtb')
        res = Voice.objects.filter(vtb_name=vtb, group='default')
    else:
        res = Voice.objects.filter(group='default')
    res_list = []
    for item in res:
        res_list.append({
            'name': item.name,
            'vtuber': item.vtb_name,
            'group': item.group,
            'id': item.id,
            'url': item.url,
            'tag': item.tag
        })
    return response_json({'code': 200, 'message': '操作成功', 'data': res_list})


# 变更voice属性
def change_voice(request):
    if not request.user.has_perm('DataBaseModel.change_voice'):
        return response_json({'code': 403, 'message': '权限不足'})
    to_change_id = int(request.POST.get('aim'))
    obj = Voice.objects.get(id=to_change_id)
    if request.POST.get('vtb'):
        obj.vtb_name = request.POST.get('vtb')
        obj.group = 'default'
    if request.POST.get('group'):
        obj.group = request.POST.get('group')
    if request.POST.get('name'):
        obj.name = request.POST.get('name')
    if request.POST.get('tag'):
        obj.tag = request.POST.get('tag')
    obj.save()
    return response_json({'code': 200, 'message': '操作成功'})


# TODO: 更新翻译系统
# 查询语音
def get_voice(request):
    vtb = request.GET.get('vtb-name')
    if request.GET.get('group'):
        group_name = request.GET.get('group')
        voices = Voice.objects.filter(vtb_name=vtb, group=group_name)
        groups = VoiceGroup.objects.filter(vtb_name=vtb, group_name=group_name).first()
        if not voices:
            return response_json({'message': '未找到数据'})
        group = []
        for voice in voices:
            tmp = {
                'data_id': voice.id,
                'name': voice.name,
                'path': voice.url,
                'click_count': voice.count,
                'translation': translate.get_translate(voice.name, 'voice'),
                'tag': voice.tag
            }
            group.append(tmp)
        response = {
            'name': groups.group_name,
            'translation': translate.get_translate(groups.group_name, 'group'),
            'all_click_count': groups.all_count,
            'voicelist': group
        }
        return response_json(response)

    groups = VoiceGroup.objects.filter(vtb_name=vtb)
    data = Voice.objects.filter(vtb_name=vtb)
    if not data:
        return response_json({'message': '未找到数据'})

    group2 = []
    for group in groups:
        voice_list = []
        name = group.group_name
        voices = Voice.objects.filter(group=name, vtb_name=vtb)
        for voice in voices:
            voice_list.append({
                'data_id': voice.id,
                'name': voice.name,
                'path': voice.url,
                'click_count': voice.count,
                'translation': translate.get_translate(voice.name, 'voice'),
                'tag': voice.tag
            })
        group_item = {
            'name': group.group_name,
            'translation': translate.get_translate(group.group_name, 'group'),
            'all_click_count': group.all_count,
            'voicelist': voice_list
        }
        group2.append(group_item)
    response = {
        'last_update': '不详',
        'groups': group2
    }
    return response_json(response)


def delete_voice(request):
    if not request.user.has_perm('DataBaseModel.delete_voice'):
        return response_json({'code': 403, 'message': '权限不足'})
    id = request.GET.get('id')
    Voice.objects.get(id=id).delete()
    return response_json({'code': 200, 'message': '删除成功'})


# 清除版本
def next_ver(request):
    if not request.user.has_perm('DataBaseModel.add_voice'):
        return response_json({'code': 403, 'message': '权限不足'})
    vtb_name = request.POST.get('vtb')
    # 版本控制
    print(vtb_name)
    version_control(vtb_name, '1')
    return response_json({'code': 200, 'message': '操作成功'})
