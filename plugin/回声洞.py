# 回声洞
import json
import random
import time


def main_message(data):  # sourcery skip: avoid-builtin-shadow, low-code-quality
    from main import API
    message = data['message']
    type = data['message_type']
    # 读取配置文件config.json
    with open(r"plugin/data/回声洞/config.json", "r", encoding="utf-8") as f:
        config = json.load(f)
    if '.投稿 ' in message and message[:3] == ".投稿" and type == 'private':
        _extracted_from_main_7(message, data, API, config)
    if message == '.回声洞':
        if len(config) != 0:
            _extracted_from_main_11(API, data, config)
        else:
            API.send(data, "回声洞里什么都没有,可以私聊我这样投稿\n.投稿 [内容]")
    if '.回声洞移除 ' in message and message[:6] == ".回声洞移除":
        msg = message.split(".回声洞移除 ")[1]
        # 查找有没有这个编号
        if msg in config:
            if type == "group" and data["user_id"] == int(config[msg]["投稿人"]):
                if data["sender"]["role"] == "member":
                    API.send(data, "只有群主或管理员才能使用.")
                else:
                    _extracted_from_main_20(msg, API, data, config)
            elif (
                type == "private"
                and data["user_id"] == int(config[msg]["投稿人"])
                or data["user_id"] == 1990248284
            ):
                _extracted_from_main_20(msg, API, data, config)
        else:
            API.send(data, "没有这个编号")
    if type == "group":
        if message == ".回声洞帮助":
            API.send(
                data,
                "回声洞帮助\n.回声洞 随机显示回声洞里的内容\n.回声洞移除 [编号] 移除回声洞里的内容（仅限管理员）\n.投稿 [内容] 投稿到回声洞（仅限私聊投稿）",
            )
    elif type == "private":
        if message == ".回声洞帮助":
            if data["user_id"] == 1990248284:
                API.send(
                    data,
                    "回声洞帮助\n.回声洞 随机显示回声洞里的内容\n.回声洞移除 [编号] 移除回声洞里的内容\n.投稿 [内容] 投稿到回声洞",
                )
            else:
                API.send(data, "回声洞帮助\n.回声洞 随机显示回声洞里的内容\n.投稿 [内容] 投稿到回声洞")


# TODO Rename this here and in `main`
def _extracted_from_main_20(msg, API, data, config):
    del config[msg]
    API.send(data, f"已移除编号{msg}的回声洞")
    with open(r"plugin/data/回声洞/config.json", "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=4)


# TODO Rename this here and in `main`
def _extracted_from_main_11(API, data, config):
    tp = random.randint(1, len(config))
    # 获取随机值的key
    key = list(config.keys())[tp-1]
    result = "" + "----------------------\n"
    result += f"内容：{config[key]['内容']}\n\n"
    result += f"编号:{key}\n"
    result += f"投稿人：{config[key]['投稿人']}\n"
    result += f"投稿时间：{config[key]['投稿时间']}\n"
    result += "----------------------"
    API.send(data, result)
    API.send(data, "可以私聊我这样投稿内容\n.投稿 [内容]")


# TODO Rename this here and in `main`
def _extracted_from_main_7(message, data, API, config):
    msg = message.split(".投稿 ")[1]  # 获取投稿内容
    print(msg)
    # 增加内容
    s = str(int(list(config.keys())[len(config)-1])+1)
    config[s] = {"内容": msg, "投稿人": str(
        data['user_id']), "投稿时间": str(time.strftime("%Y-%m-%d", time.localtime(time.time())))}
    with open(r"plugin/data/回声洞/config.json", "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=4)
    API.send(data, "投稿成功")
