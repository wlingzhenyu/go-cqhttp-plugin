from faker import Faker
faker = Faker(locale='zh_CN')


def main_message(data):
    from main import API
    message = data['message']
    if message == '生成伪造信息':
        API.send(
            data, f'伪造信息：\n姓名：{faker.name()}\n身份证：{faker.credit_card_number()}[请忽略这项，这个有可能是错误的！]\n住址：{faker.address()}\n电话：{faker.phone_number()}\n邮箱：{faker.email()}\n公司：{faker.company()}\n职位：{faker.job()}\n网名：{faker.user_name()}')
