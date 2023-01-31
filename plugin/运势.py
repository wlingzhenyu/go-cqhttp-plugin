import configparser
import os
import random
import time

cf = configparser.ConfigParser(default_section="run")
cf2 = configparser.ConfigParser(default_section="write")
proDir = os.path.split(os.path.realpath(__file__))[0]
configPath = os.path.join(proDir + r"\data\运势", "Fortune.ini")
configPath2 = os.path.join(proDir + r"\data\运势", "MemberData.ini")


def main_message(data):
    from main import API

    message = data['message']
    if message == "今日运势":
        cf2.read(configPath2, encoding="utf-8")
        qqid = data['user_id']
        if not cf2.has_section(str(qqid)):
            cf2.add_section(str(qqid))
        cf2.set(
            str(qqid),
            "id",
            _extracted_from_menu_5(data['message_type'], qqid, data, API),
        )
        cf2.set(
            str(qqid), "time", time.strftime(
                "%Y-%m-%d", time.localtime(time.time()))
        )
        cf2.write(open(configPath2, 'r+'))


# TODO Rename this here and in `menu`
def _extracted_from_menu_5(type, qqid, data, API):

    cf.read(configPath, encoding="utf-8")
    r = random.randint(1, len(cf.sections()))
    # r = 67
    if cf2.has_section(str(qqid)) and cf2.has_option(str(qqid), "id"):
        if cf2.get(str(qqid), "time") < time.strftime(
            "%Y-%m-%d", time.localtime(time.time())
        ):
            result2 = str(r)
        else:
            result2 = cf2.get(str(qqid), "id")
    else:
        result2 = str(r)
    result = cf.options(result2)
    result = (
        cf.get(result2, result[0])
        + "\n"
        + cf.get(result2, result[1])
        + "\n"
        + cf.get(result2, result[2])
        + "\n"
        + cf.get(result2, result[3])
    )
    if type == "group":
        API.send(data, f"[CQ:at,qq={qqid}]\n{result}")
    else:
        API.send(data, result)
    return result2
