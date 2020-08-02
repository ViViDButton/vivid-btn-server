from DataBaseModel.models import Translate
from vividBtnAIO.utils import response_json


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


def del_translate(name, group):
    # Translate.objects.get(name=name, group=group).delete()
    return True


# API
def get_translate_list(request):
    if request.POST.get('type'):
        pass
    
    pass
