import time
from typing import List

import requests

from auto_cube import MOUSE_X, MOUSE_Y, check_result1
from src.common import vkeys
from src.modules.myListener import Listener

MIAO_CODE = 'tvHK4mP'  # string，喵码。指定发出的提醒，一个提醒对应一个喵码。（必填）
STATS = ["敏捷", "力量", "最大血", "智力", "运气", "所有"]


def miao_tixing(msg):
    ts = str(time.time())  # 时间戳

    type = 'json'  # 返回内容格式

    request_url = "http://miaotixing.com/trigger?"

    # 伪装一个浏览器头发送请求（反爬的一个习惯操作，实际上不加请求头伪装也可以使用）
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36 Edg/87.0.664.47'}

    response = requests.post(request_url + "id=" + MIAO_CODE + "&text=" + msg + "&ts=" + ts + "&type=" + type,
                             headers=headers)

    if response.status_code == 200:
        result = response.json()
        print(result)
    else:
        print("请求失败")



if __name__ == '__main__':
    listener = Listener()
    listener.start()
    listener.enabled = True
    while not listener.ready:
        time.sleep(0.01)
    # while True:
    #     vkeys.click(15, 15)
    wanna_result = [["敏捷", "敏捷", "敏捷"], ["力量", "力量", "力量"], ["智力", "智力", "智力"],
                    ["运气", "运气", "运气"], ["所有", "所有", "所有"]]
    result = ['所有属性：+5%', '角色每10级力量：+1', '力量:+5%']
    check_result1(result, wanna_result)

    # miao_tixing("测试")
