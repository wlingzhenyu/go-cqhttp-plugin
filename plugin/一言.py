# 获取api,url = https://v1.hitokoto.cn/?encode=text
import requests


def main_message(data):
    from main import API
    message = data['message']
    if message == '一言':
        api = 'https://v1.hitokoto.cn'
        # 获取api，json
        api_data = requests.get(api).json()
        API.send(data, api_data['hitokoto'] + "  ——" + api_data['from'])
