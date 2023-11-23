import time
from typing import List

import requests

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


def check_result1(result: List[str], wanna_result: List[List[str]]) -> bool:
    """
    检查 result 中是否包含 wanna_result 元素其中一个结果组合
    wanna_result: [["敏捷", "敏捷", "敏捷"], ["力量", "力量", "力量"], ["智力", "智力", "智力"], ["力量", "力量", "力量"]]
    wanna_result: [["敏捷", "力量", "最大血", "智力", "运气", "所有"]]
    """
    """
    检查 result 中是否包含 wanna_result 元素其中一个结果组合
    """
    get_result = []
    # 结果预处理
    for i, r in enumerate(result):
        result[i] = result[i].replace("里", "量")
        result[i] = result[i].replace("童", "量")
        result[i] = result[i].replace(" ", "")
        get_result.append(result[i])
        if "%" not in r and "级" not in r:
            result[i] = ""
            continue
    print(f"当前结果：{get_result}")
    print(f"修正结果：{result}")

    # 遍历 wanna_result 中的每个结果组合
    copy_result = result.copy()
    for combination in wanna_result:
        match_count = 0  # 记录匹配的结果数量
        for wanna in combination:
            for i, r in enumerate(copy_result):
                if "所有" in r and wanna in STATS:
                    match_count += 1
                    copy_result[i] = ""
                elif wanna in r:
                    match_count += 1
                    copy_result[i] = ""

        if match_count == len(combination):
            print("匹配成功！")
            return True
    print("匹配失败！")
    return False


if __name__ == '__main__':
    wanna_result = [["敏捷", "敏捷", "敏捷"], ["力量", "力量", "力量"], ["智力", "智力", "智力"],
                    ["力量", "力量", "力量"], ["所有", "所有", "所有"]]
    check_result1(['角色每10级敏捷：+2', '所有属性：+4%', '敏捷:+5%'], wanna_result)

    # miao_tixing("测试")
