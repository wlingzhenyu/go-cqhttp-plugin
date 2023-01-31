import asyncio
import contextlib
import os
import threading
import time
import importlib
import requests
from flask import Flask, request

app = Flask(__name__)


class API:
    def getapi(self, info: None = None):
        """
        获取api
        ---
        参数
            mode: str->模式.
            info: str->信息 = None.

        返回：json
        """
        if self == "get_stranger_info":
            params = {"user_id": info, "no_cache": False}
            url = "http://127.0.0.1:5700/get_stranger_info"
        return requests.get(url, params=params).json()

    def send(self, message: str):
        """
        发送消息
        ---

        参数
            data: list->消息数据.
            message: str->消息内容.

        返回：无
        """
        sub_type = self['sub_type']
        if sub_type == 'friend':
            params = {
                "message_type": 'private',
                "user_id": self['user_id'],
                "message": message,
            }
            pmode = "私聊"
        elif sub_type == 'group':
            params = {
                "message_type": 'private',
                "user_id": self['user_id'],
                "message": message,
            }
            pmode = "临时消息"
        elif sub_type in ['normal', "set", "unset", "kick", "leave", "approve", "invite"]:
            params = {
                "message_type": 'group',
                "group_id": self['group_id'],
                "message": message,
            }
            pmode = "群聊消息"
        url = "http://127.0.0.1:5700/send_msg"
        requests.get(url, params=params)
        print(f"已处理，模式为{pmode} 参数为{params}")

    def request(self, approve: bool = True):
        """
        处理请求
        ---

        参数
            data: dict->请求数据.
            approve: bool->是否同意 = True.

        返回：无
        """
        if self['request_type'] == 'friend':  # 判断消息类型 如果是好友请求
            params = {"flag": str(self['flag']), "approve": approve}
            pmode = "好友请求"
            url = "http://127.0.0.1:5700/set_friend_add_request"
        elif self['request_type'] == 'group':
            params = {
                "flag": str(self['flag']),
                "sub_type": self['sub_type'],
                "approve": approve,
            }
            pmode = "群申请"
            url = "http://127.0.0.1:5700/set_group_add_request"
        requests.get(url, params=params)
        print(f"已处理，模式为{pmode} 参数为{params}")


def process_message(data):
    """处理消息"""
    for i in range(len(plugin_list)):
        with contextlib.suppress(Exception):
            threading.Thread(
                target=eval(f"{plugin_list[i]}.main_message"),
                args=(data,),
                daemon=True,
            ).start()


def process_notice(data):
    """处理消息"""
    for i in range(len(plugin_list)):
        with contextlib.suppress(Exception):
            threading.Thread(
                target=eval(f"{plugin_list[i]}.main_notice"), args=(
                    data,), daemon=True  # 设置守护线程
            ).start()


def process_request(data):
    """处理消息"""
    for i in range(len(plugin_list)):
        # 尝试执行，报错没关系
        with contextlib.suppress(Exception):
            threading.Thread(
                target=eval(f"{plugin_list[i]}.main_request"), args=(
                    data,), daemon=True  # 设置守护线程
            ).start()


@app.route('/', methods=["POST"])
def post_data():
    """接收并处理消息和事件"""
    data = request.get_json()
    print(data)
    # if data['post_type'] != 'meta_event':  # 判断消息类型 如果是私聊消息
    #     print(data)
    if data['post_type'] == 'message':  # 判断消息类型 如果是私聊消息
        if data['sub_type'] == 'group' and data['message_type'] == "private":
            API.send(data, message="那个...能先加我好友吗，我不太会用群临时功能欸...")
        else:
            process_message(data)
    elif data['post_type'] == 'request':
        process_request(data)
    elif data['post_type'] == 'notice':
        process_notice(data)
    return "ok"


async def load_plugin(i):
    spec = importlib.util.find_spec(f"plugin.{i.name[:-3]}")
    if spec is not None:
        globals()[i.name[:-3]
                  ] = importlib.import_module(f"plugin.{i.name[:-3]}")
        return i.name[:-3]

if __name__ == '__main__':
    plugin_list = []
    loop = asyncio.get_event_loop()
    plugin_list = loop.run_until_complete(asyncio.gather(
        *[load_plugin(i) for i in os.scandir("plugin") if i.name.endswith(".py") and i.is_file()]))
    app.run(port=5701, host='127.0.0.1')
