from vividBtnAIO.utils import upyunAccount
from vividBtnAIO import utils
from DataBaseModel.models import Voice, VoiceGroup, Vtuber, Translate
import json
import upyun

# TODO: 封装upyun上传文件的库
# 统计

def item_click(request):
    id = request.GET.get('id')
    item = Voice.objects.filter(id=id).first()
    item.count = item.count + 1
    item2 = VoiceGroup.objects.filter(group_name=item.group).first()
    item2.all_count = item2.all_count + 1
    item.save()
    item2.save()
    return utils.response_json({'count': item.count, 'group_all_count': item2.all_count})

# 开发时使用，发布请删掉
def del_all(request):
    if not request.GET.get('confirm'):
        return utils.response_json({'Warning': '你真的要这么做吗，确定请加confirm参数！', 'message': '正义提醒您：删库一时爽，一直删库一直爽！'}, 400)
    Voice.objects.all().delete()
    VoiceGroup.objects.all().delete()
    Vtuber.objects.all().delete()
    Translate.objects.all().delete()
    return utils.response_json({'Warning': '删库跑路'})
