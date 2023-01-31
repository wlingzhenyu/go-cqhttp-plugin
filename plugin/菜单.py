def main_message(data):
    from main import API
    message = data['message']
    if message == '菜单':
        result = '----------------------\n' + '菜单\n'
        result += '----------------------\n'
        if data['sub_type'] == 'normal':
            if data['group_id'] in [1142570642, 530335513, 595143383]:
                result += '今日聊天记录\n'
                result += '.签到\n'
                result += '.QID (绑定码)\n'
                result += '在线玩家\n'
                result += '发送到服务器 【文字】\n'
                result += '执行指令 /【指令】\n'
            if data['group_id'] in [310839897]:
                result += '服务器信息\n'
        result += '生成伪造信息\n'
        result += '一言\n'
        result += '.回声洞帮助\n'
        result += '今日运势\n'
        result += '今日词云图\n'
        result += '随机二次元图片\n'
        result += '----------------------\n'
        API.send(data, result)
