def main_notice(data):
    from main import API
    if data['notice_type'] == 'group_admin':
        if data['sub_type'] == 'set':
            nickname = API.getapi("get_stranger_info", info=data['user_id'])['data'][
                'nickname']
            API.send(data, f"恭喜{data['user_id']}[{nickname}]成为管理员")
        elif data['sub_type'] == 'unset':
            nickname = API.getapi("get_stranger_info", info=data['user_id'])['data'][
                'nickname']
            API.send(data, f"很遗憾{data['user_id']}[{nickname}]被取消管理员")
    elif data['notice_type'] == 'group_increase':
        if data['sub_type'] == 'approve':
            API.send(data, f"欢迎[CQ:at,qq={data['user_id']}]加入本群")
        elif data['sub_type'] == 'invite':
            nickname2 = API.getapi("get_stranger_info", info=data['operator_id'])['data'][
                'nickname']
            API.send(
                data, f"欢迎[CQ:at,qq={data['user_id']}]被邀请加入本群\n邀请人：{data['operator_id']}[{nickname2}]]")
    elif data['notice_type'] == 'group_decrease':
        if data['sub_type'] == 'kick':
            nickname = API.getapi("get_stranger_info", info=data['user_id'])['data'][
                'nickname']
            API.send(data, f"{data['user_id']}[{nickname}]被管理炫出群了")
        elif data['sub_type'] == 'leave':
            nickname = API.getapi("get_stranger_info", info=data['user_id'])['data'][
                'nickname']
            API.send(data, f"{data['user_id']}[{nickname}]似乎离开了本群...")
