from typing import List
import time

from cnocr import CnOcr
import win32gui
import cv2
import numpy as np
import pyautogui
import requests

from src.common import config, vkeys
from src.common.utils import run_if_enabled
from src.modules.myListener import Listener

MOUSE_X, MOUSE_Y = 662, 543  # 再来一次魔方相对坐标
LEFT, TOP, RIGHT, BOTTOM = 608, 456, 774, 501  # 魔方结果相对坐标
STATS = ["敏捷", "力量", "最大血", "智力", "运气", "所有"]
MIAO_CODE = 'tvHK4mP'  # string，喵码。指定发出的提醒，一个提醒对应一个喵码。（必填）
BIG_RESULT = ["7%", "+2", "8%", "冷却"]
SMALL_RESULT = ["5%", "+1", "4%", "6%"]


def is_repeated_n_times(string, char, n):
    count = string.count(char)
    return count == n


@run_if_enabled
def check_result1(result: List[str], wanna_result: List[List[str]], wanna_size: int) -> bool:
    """
    检查 result 中是否包含 wanna_result 元素其中一个结果组合
    wanna_result: [["敏捷", "敏捷", "敏捷"], ["力量", "力量", "力量"], ["智力", "智力", "智力"], ["力量", "力量", "力量"]]
    wanna_result: [["敏捷", "力量", "最大血", "智力", "运气", "所有"]]
    """
    """
    检查 result 中是否包含 wanna_result 元素其中一个结果组合
    """
    print(f"想要结果组合：{wanna_result}")
    # 结果预处理
    print(f"识别结果：{result}")
    result = correct_result(result)

    # 遍历 wanna_result 判断属性
    print(f"需求评分: {wanna_size}")
    size = check_size(result)
    for combination in wanna_result:
        match_count = 0  # 记录匹配的结果数量
        copy_result = result.copy()
        for wanna in combination:
            for i, r in enumerate(copy_result):
                if "属性" in r and wanna in STATS:
                    match_count += 1
                    copy_result[i] = ""
                elif wanna in r:
                    match_count += 1
                    copy_result[i] = ""

        if match_count == len(combination) and size >= wanna_size:
            # 判断大小
            print("行数匹配成功！")
            result.append(size)  # 调试使用
            result.append(size >= wanna_size)  # 调试使用
            return True
    size_result = "评分匹配成功！" if size >= wanna_size else "评分匹配失败！"
    print(size_result)
    print("行数匹配失败！")
    return False


def correct_result(result):
    get_result = []
    for i, r in enumerate(result):
        result[i] = result[i].replace("里", "量")
        result[i] = result[i].replace("童", "量")
        result[i] = result[i].replace("单", "量")
        result[i] = result[i].replace(" ", "")
        get_result.append(result[i])
        if (("%" not in r and "级" not in r)):
                # or ("级" in r and "+1" in r)):
            result[i] = ""
            continue
    print(f"修正结果：{result}")
    return result


def check_size(result, wanna_size=200):
    size = 0
    for r in result:
        if any(s in r for s in BIG_RESULT):
            size += 100
        elif any(s in r for s in SMALL_RESULT):
            size += 10
    print(f"结果评分：{size}")
    return size


@run_if_enabled
def cube_one(hwnd):
    window_rect = win32gui.GetWindowRect(hwnd)
    window_left, window_top, _, _ = window_rect
    pyautogui.leftClick(MOUSE_X + window_left, MOUSE_Y + window_top)  # 单击 再使用一次魔方
    vkeys.click([MOUSE_X + window_left, MOUSE_Y + window_top], "left")
    vkeys.press("enter", 3)
    time.sleep(2)


@run_if_enabled
def recognize_text_in_screen_region(ocr, hwnd, left, top, right, bottom):
    # 获取窗口位置
    window_rect = win32gui.GetWindowRect(hwnd)
    window_left, window_top, _, _ = window_rect

    # 捕获屏幕区域图像
    screenshot = pyautogui.screenshot()
    image = np.array(screenshot)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    # 计算相对坐标
    region_left = window_left + left
    region_top = window_top + top
    region_right = window_left + right
    region_bottom = window_top + bottom

    # 裁剪图像为指定区域
    region_image = image[region_top:region_bottom, region_left:region_right]
    # 按行截图
    line1 = region_image[0:15, :]
    line2 = region_image[15:30, :]
    line3 = region_image[30:region_bottom - region_top, :]
    # 显示图像
    lines = [line1, line2, line3]
    result = []
    for line in lines:
        # 进行文字识别
        r = ocr.ocr_for_single_line(line)
        result.append(r.get("text"))
    # show_image(region_image)
    return result


def show_image(img):
    # 创建窗口并展示图像
    # cv2.namedWindow("img ", cv2.WINDOW_NORMAL)
    cv2.imshow("img", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def auto_cube(ocr, hwnd, wanna_result: List, wanna_size: int):
    while True:
        cube_one(hwnd)
        result = recognize_text_in_screen_region(ocr, hwnd, LEFT, TOP, RIGHT, BOTTOM)
        if check_result1(result, wanna_result, wanna_size):
            config.enabled = False
            miao_tixing(f"出货了{result}")
        # print(t1- time.time())

        time.sleep(0.1)


def init_hwnd():
    # 根据窗口标题查找窗口句柄
    hwnd = win32gui.FindWindow("MapleStoryClass", "MapleStory")

    if hwnd != 0:
        # 获取外部程序的窗口句柄
        window_handle = pyautogui.getWindowsWithTitle('MapleStory')[0]
        # 找到了窗口句柄，将窗口移动到 (0, 0) 位置
        window_handle.moveTo(0, 0)  # 设置新的窗口位置坐标
        print("初始化成功！")
        return hwnd
    else:
        print("窗口未找到，5秒后继续查找")
        time.sleep(5)
        init_hwnd()


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
    hwnd = init_hwnd()
    # 只检测和识别水平文字
    cn_ocr = CnOcr(rec_model_name='densenet_lite_136-fc', det_model_name='db_shufflenet_v2_small',
                   det_model_backend="pytorch", det_more_configs={'rotated_bbox': False})
    listener = Listener()
    listener.start()
    while not listener.ready:
        time.sleep(0.01)
    listener.enabled = True
    #
    wanna_result = [["敏捷", "敏捷", "敏捷"], ["力量", "力量", "力量"], ["智力", "智力", "智力"],
                    ["运气", "运气", "运气"], ["所有", "所有", "所有"]]
    # #
    # # wanna_result = [["敏捷", "敏捷"], ["力量", "力量"], ["智力", "智力"],
    # #                 ["力量", "力量"], ["所有", "所有"]]
    # # wanna_result = [["敏捷", "敏捷", "敏捷"]]
    # # wanna_result = [["攻击力", "攻击力"]]

    auto_cube(cn_ocr, hwnd, wanna_result, 200)
    # config.enabled = True
    # check_result1(["敏捷：+7%", "每级敏捷：+2", "每级敏捷：+2"], wanna_result, 200)

    # config.enabled = True
    # t1 = time.time()
    # r = check_result1(result=["敏捷：+7", "所有属性：+4%", "每10级敏捷：+2"],
    #                   wanna_result=[["敏捷", "敏捷", "敏捷"], ["力量", "力量", "力量"], ["智力", "智力", "智力"],
    #                                 ["力量", "力量", "力量"], ["所有", "所有", "所有"]])
    # print(f"r={r}")
    # print(time.time() - t1)
    # auto_cube(cn_ocr, ["敏捷", "力量", "最大血", "智力", "运气", "所有"])
    # check_result("敏捷：+7%;智力:+16;角色每10级敏捷：+1")
