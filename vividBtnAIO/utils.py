from django.http import HttpResponse
from django.http import HttpResponseRedirect
import json
from configparser import ConfigParser

config = ConfigParser()
config.read('config/config.ini', encoding='UTF-8')
upyunAccount = config['UpYunAccount']


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
