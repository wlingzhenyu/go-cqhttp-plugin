def main_request(data):
    if data['user_id'] not in [] or data['group_id'] not in []:
        from main import API
        API.request(data, True)
