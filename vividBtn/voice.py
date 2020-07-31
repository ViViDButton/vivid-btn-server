from vividBtnAIO.utils import upyunAccount, response_json
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
    try:
        file_name = file_obj.name.replace('"', ' ').rstrip().lstrip()
        file_name_splited = file_name.split('.')
        extend_name = file_name_splited[len(file_name_splited) - 1].rstrip().lstrip()
        extend_name_list = ['mp3', 'wav']
    except:
        return response_json({'message': '无法解析文件'}, 403)
    if not (extend_name in extend_name_list):
        return response_json({'message': '不允许的文件格式'}, 403)

    # 文件保存
    f = open('cache/' + file_name, 'wb')
    for chuck in file_obj.chunks():
        f.write(chuck)
    f.close()

    # 文件上传
    headers = {}
    with open('cache/' + file_name, 'rb') as f:
        try:
            res = up.put(file_path + vtb_name + '/voice/' + group + '/' + file_name, f, checksum=True,
                         headers=headers)
            res = up.getinfo(file_path + vtb_name + '/voice/' + group + '/' + file_name)
            print(res)
        except Exception as e:
            print(str(e))
            return response_json({'message': '上传失败', 'error': str(e)}, 403)
    url = 'https://' + upyun_url + file_path + vtb_name + '/voice/' + group + '/' + file_name

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


#
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
                'translation': json.loads(voice.translate)
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
            tmp = {
                'data_id': voice.id,
                'update': voice.version,
                'name': voice.name,
                'path': voice.url,
                'click_count': voice.count,
                'translation': json.loads(voice.translate)
            }
            voice_list.append(tmp)
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

