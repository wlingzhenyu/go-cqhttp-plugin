from mcstatus import JavaServer


def main_message(data):
    from main import API
    message = data['message']
    if data['sub_type'] == 'normal' and data['group_id'] in [310839897, 759071494] and message == '服务器信息' or message == '服务器状态':
        try:
            if data['group_id'] == 310839897:
                serverip = 'game.tblstudio.cn'
            elif data['group_id'] == 759071494:
                serverip = 'play.simpfun.cn:25570'
            server = JavaServer.lookup(serverip)
            status = server.status()
            query = server.query()
            API.send(
                data, f'在线人数：{status.players.online}/{status.players.max}\n服务器延迟：{int(status.latency)} ms\n服务器版本：{status.version.name}\n服务器有以下玩家在线：\n{",".join(query.players.names)} ')
        except Exception as err:
            API.send(data, '服务器查询失败，有可能不在线')
            print(err)
