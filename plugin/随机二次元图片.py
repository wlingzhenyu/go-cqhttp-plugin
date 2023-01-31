import random

import requests


def main_message(data):
    from main import API

    if data['message'] == '随机二次元图片':
        url = 'https://api.vvhan.com/api/acgimg'
        params = {'type': 'json'}
        res = requests.get(url, params=params).json()
        print(res)
        API.send(data, f"""[CQ:image,file={res['imgurl']}]""")
