import os
import time
from wordcloud import WordCloud
import jieba


def main_message(data):
    from main import API

    message = data['message']
    # 如果message不包含[CQ: 或者 今日词云图 就存入
    if "[CQ:" not in message and "今日词云图" not in message:
        # 判断 词云图.txt 第一行的日期是否为今天的，不是就删 然后写入信息
        with open("plugin/data/词云图/词云图.txt", "r", encoding="utf-8") as f:
            if time.strftime("%Y-%m-%d", time.localtime()) not in f.readline():
                with open("plugin/data/词云图/词云图.txt", "w", encoding="utf-8") as f:
                    f.write(time.strftime("%Y-%m-%d", time.localtime()) + "\n")
        # 写入信息
        with open("plugin/data/词云图/词云图.txt", "a", encoding="utf-8") as f:
            f.write(message + "\n")
    # 如果message包含 今日词云图 就执行
    if message == "今日词云图":
        _extracted_from_main_11(API, data)


# TODO Rename this here and in `main`
def _extracted_from_main_11(API, data):
    # 读取文件 一行一行拼接为一句 jieba分词 读取时排除第一行 利用C:\Users\Administrator\Desktop\机器\go-cqhttp\plugin\data\词云图\停用词.txt
    with open("plugin/data/词云图/词云图.txt", "r", encoding="utf-8") as f:
        text = "".join(f.readlines()[1:])
    text = " ".join(jieba.cut(text))
    with open("plugin/data/词云图/停用词.txt", "r", encoding="utf-8") as f:
        stop_words = f.read()
    # 判断text是否为空
    if text != "":
        # 生成词云图 微软雅黑字体
        # 利用API发送图片
        WordCloud(
            font_path="C:\Windows\Fonts\msyh.ttc",
            background_color='#F3F3F3',
            stopwords=stop_words,
            width=1600,
            height=900,
        ).generate(text).to_file("plugin/data/词云图/词云图.png")
        # plugin/data/词云图/词云图.png 的绝对路径转换为完整路径并且发出照片
        API.send(
            data,
            f"[CQ:image,file=file:///{os.path.abspath('plugin/data/词云图/词云图.png')}]",
        )
    else:
        API.send(data, "今日词云图为空")
