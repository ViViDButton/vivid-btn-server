from vividBtnAIO.utils import upyunAccount, response_json
from DataBaseModel.models import Voice, VoiceGroup, Vtuber
import json
import upyun

# TODO: 封装upyun上传文件的库

# 开源时务必删除账户信息
up = upyun.UpYun(upyunAccount['service'], upyunAccount['username'], upyunAccount['password'])
upyun_url = upyunAccount['upyun_url']
file_path = upyunAccount['file_path']


def get_vtb(request):
    vtubers_list = Vtuber.objects.all()
    vtb = []
    for vtuber in vtubers_list:
        tmp = {
            'name': vtuber.name,
            'bili-id': vtuber.bilibili_uid,
            'youtube-id': vtuber.youtube_id
        }
        vtb.append(tmp)
    return response_json({'code': 200, 'list': vtb})


def add_vtuber(request):
    if request.method == 'GET':
        return response_json({'message': '请使用POST方法'}, 403)
    if not request.user.has_perm('DataBaseModel.add_vtuber'):
        return response_json({'code': 403, 'message': '权限不足'})
    name = request.POST.get('name')
    bili_id = int(request.POST.get('bili-id'))
    youtube_id = request.POST.get('youtube-id')
    if Vtuber.objects.filter(name=name):
        return response_json({'message': '该Vtuber已经存在'}, 403)
    vtuber = Vtuber(name=name, bilibili_uid=bili_id, youtube_id=youtube_id)
    vtuber.save()
    return response_json({'message': '操作成功'})

def delete_vtb(request):
    if not request.user.has_perm('DataBaseModel.delete_vtuber'):
        return response_json({'code': 403, 'message': '权限不足'})
    name = request.GET.get('name')
    Vtuber.objects.get(name=name).delete()
    VoiceGroup.objects.filter(vtb_name=name).delete()
    Voice.objects.filter(vtb_name=name).delete()
    return response_json({'code': 200, 'message': '删除成功'})

