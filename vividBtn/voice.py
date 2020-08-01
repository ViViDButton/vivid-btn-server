from vividBtnAIO.utils import upyunAccount, response_json, handle_pic_upload
from DataBaseModel.models import Voice, VoiceGroup, Vtuber
import json
import upyun

# TODO: 封装upyun上传文件的库

# 开源时务必删除账户信息
up = upyun.UpYun(upyunAccount['service'], upyunAccount['username'], upyunAccount['password'])
upyun_url = upyunAccount['upyun_url']
file_path = upyunAccount['file_path']


def add_voice_data(request):
    if request.method == 'GET':
        return response_json({'message': '请使用POST方法'}, 403)
    if not request.user.has_perm('DataBaseModel.add_voice'):
        return response_json({'code': 403, 'message': '权限不足'})
    vtb_name = request.POST.get('vtb-name')
    name = request.POST.get('voice-name')
    group = request.POST.get('group-name')
    file_obj = request.FILES.get('file')

    # 文件类型校验

    url = handle_pic_upload(file_obj, vtb_name=vtb_name, group=group)

    if url['code'] == 403:
        return response_json(url)

    url = url['url']

    version = request.POST.get('ver')
    count = 0
    zh = request.POST.get('zh')
    ja = request.POST.get('ja')
    en = request.POST.get('en')
    # 检查是否有本vtb
    if not Vtuber.objects.filter(name=vtb_name):
        return response_json({'message': '请先创建此vtuber'}, 403)
    if not VoiceGroup.objects.filter(group_name=group):
        return response_json({'message': '没有此分组!'}, 403)
    translate = {'zh': zh, 'ja': ja, 'en': en}
    voice = Voice(vtb_name=vtb_name, name=name, group=group, url=url, version=version, count=count
                  , translate=json.dumps(translate))
    voice.save()
    return response_json({'message': '操作成功', 'file_locate': url})


# 批量上传
def batch_upload(request):
    if not request.user.has_perm('DataBaseModel.add_voice'):
        return response_json({'code': 403, 'message': '权限不足'})
    upload_resp = handle_pic_upload(request.FILES.get('file'))
    if request.POST.get('vtuber') != '':
        vtb_name = request.POST.get('vtuber')
    else:
        vtb_name = 'default'
    name = upload_resp['file_name']
    url = upload_resp['url']

    voice = Voice(vtb_name=vtb_name, name=name, group='default', url=url, count=0)
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
            'url': item.url
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
                'update': voice.version,
                'name': voice.name,
                'path': voice.url,
                'click_count': voice.count,
                'translation': 'json.loads(voice.translate)'
            }
            group.append(tmp)
        response = {
            'name': groups.group_name,
            'translation': json.loads(groups.translate),
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
                'update': 'voice.version',
                'name': voice.name,
                'path': voice.url,
                'click_count': voice.count,
                'translation': 'json.loads(voice.translate)'
            })
        group_item = {
            'name': group.group_name,
            'translation': json.loads(group.translate),
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
    Voice.objects.filter(id=id).delete()
    return response_json({'code': 200, 'message': '删除成功'})

