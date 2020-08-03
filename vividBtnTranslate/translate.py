from DataBaseModel.models import Translate
from vividBtnAIO.utils import response_json, to_list
import json


# utils Class
def add_translate(request, name, group):
    try:
        if Translate.objects.get(name=name, group=group):
            return False
    except:
        pass
    if not request.POST.get('zh'):
        zh = name
    else:
        zh = request.POST.get('zh')
    if not request.POST.get('ja'):
        ja = name
    else:
        ja = request.POST.get('ja')
    if not request.POST.get('en'):
        en = name
    else:
        en = request.POST.get('en')
    if zh == '':
        zh = name
    if ja == '':
        ja = zh
    if en == '':
        en = zh
    # try:
    translate = Translate(name=name, group=group, zh=zh, ja=ja, en=en)
    translate.save()
    # except:
    #     return False
    return True


def get_translate(name, group):
    translate = Translate.objects.get(name=name, group=group)
    return {
        'zh': translate.zh,
        'ja': translate.ja,
        'en': translate.en
    }


# FIXME: 有严重bug,暂时停用
def del_translate(name, group):
    # Translate.objects.get(name=name, group=group).delete()
    return True


# API  type: 翻译状态
def get_translate_list(request):
    if not request.user.has_perm('DataBaseModel.view_translate'):
        return response_json({'code': 403, 'message': '拒绝访问'})
    if request.POST.get('type'):
        pass
    translate_list = Translate.objects.all()
    translate = []
    for translate_item in translate_list:
        translate.append({
            'id': translate_item.id,
            'name': translate_item.name,
            'zh': translate_item.zh,
            'ja': translate_item.ja,
            'en': translate_item.en,
            'status': translate_item.status
        })
    return response_json({'code': 200, 'message': '操作成功', 'data': translate})


# API 提交翻译--日志方式
def submit_translate_log(request):
    if not request.user.has_perm('DataBaseModel.change_translate'):
        return response_json({'code': 403, 'message': '拒绝访问'})
    if not request.POST.get('log'):
        return response_json({'code': 403, 'message': '请提交翻译日志'})
    log = json.loads(request.POST.get('log'))['log']
    response_log = []
    for step in log:
        item = Translate.objects.get(id=step['id'])
        value = step['value']
        if value == '':
            value = item.name
        if step['lang'] == 'zh':
            item.zh = value
        if step['lang'] == 'ja':
            item.ja = value
        if step['lang'] == 'en':
            item.en = value
        if item.ja != item.name and item.en != item.name:
            item.status = 'done'
        item.save()
    return response_json({'code': 200, 'message': '操作成功'})


# 变更状态
def change_status(request):
    if not request.user.has_perm('DataBaseModel.change_translate'):
        return response_json({'code': 403, 'message': '拒绝访问'})
    tid = int(request.POST.get('tid'))
    if not request.POST.get('status'):
        status = 'done'
    else:
        status = request.POST.get('status')
    item = Translate.objects.get(id=tid)
    item.status = status
    item.save()
    return response_json({'code': 200, 'message': '操作成功'})


# 删除词条
