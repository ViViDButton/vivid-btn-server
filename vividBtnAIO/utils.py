from django.http import HttpResponse
from django.http import HttpResponseRedirect
import json
import os
from configparser import ConfigParser
import upyun
from DataBaseModel.models import Translate

config = ConfigParser()
config.read('config/config.ini', encoding='UTF-8')
upyunAccount = config['UpYunAccount']

# 开源时务必删除账户信息
up = upyun.UpYun(upyunAccount['service'], upyunAccount['username'], upyunAccount['password'])
upyun_url = upyunAccount['upyun_url']
file_path = upyunAccount['file_path']


def response_json(data, status=200):
    response = HttpResponse(json.dumps(data), content_type='application/json', status=status)
    # response['Access-Control-Allow-Origin'] = '*'
    # response['Access-Control-Allow-Methods'] = 'POST, GET, OPTIONS'
    # response['Access-Control-Max-Age'] = '1000'
    # response['Access-Control-Allow-Headers'] = '*'
    return response


def redirect(url):
    response = HttpResponseRedirect(url)
    response['Access-Control-Allow-Origin'] = '*'
    response['Access-Control-Allow-Methods'] = 'POST, GET, OPTIONS'
    response['Access-Control-Max-Age'] = '1000'
    response['Access-Control-Allow-Headers'] = '*'
    return response


# FIXME: 文件重复处理
def handle_pic_upload(file_obj):
    try:
        file_name = file_obj.name.replace('"', ' ').rstrip().lstrip()
        file_name_splited = file_name.split('.')
        extend_name = file_name_splited[len(file_name_splited) - 1].rstrip().lstrip()
        extend_name_list = ['mp3', 'wav']
        file_name_no_extend = os.path.splitext(file_name)[0]
    except:
        return {'code': 403, 'message': '无法解析文件'}
    if not (extend_name in extend_name_list):
        return {'code': 403, 'message': '不允许的文件格式'}

    # 文件保存
    f = open('cache/' + file_name, 'wb')
    for chuck in file_obj.chunks():
        f.write(chuck)
    f.close()

    # 文件上传
    headers = {}
    with open('cache/' + file_name, 'rb') as f:
        try:
            res = up.put(file_path + '/voice/' + file_name, f, checksum=True,
                         headers=headers)
            res = up.getinfo(file_path + '/voice/' + file_name)
        except Exception as e:
            return {'code': 403, 'message': '上传失败', 'error': str(e)}
    url = 'https://' + upyun_url + file_path + 'voice/' + file_name
    return {'code': 200, 'url': url, 'file_name': file_name_no_extend.lstrip().rstrip()}

