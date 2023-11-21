from typing import List, Dict

import cv2
import keyboard as kb
import numpy as np
import pyautogui

from cnocr import CnOcr
import time
import win32gui

from src.common import config
from src.common.utils import run_if_enabled
from src.modules.myListener import Listener

MOUSE_X, MOUSE_Y = 662, 548
LEFT, TOP, RIGHT, BOTTOM = 608, 463, 774, 508
STATS = ["敏捷", "力量", "最大血", "智力", "运气", "所有"]


def is_repeated_n_times(string, char, n):
    count = string.count(char)
    return count == n


@run_if_enabled
def check_result(result, wanna_result=None, same_line=2):
    if result:
        result.replace("力里", "力量")
        result.replace("力童", "力量")
        if wanna_result is None:
            wanna_result = ['敏捷']
        for wanna in wanna_result:
            if is_repeated_n_times(result, wanna, same_line):
                print(f"出现想要结果:{wanna}x{same_line}:结果为：{result}")
                return True
            if is_repeated_n_times(result, wanna, 2) and is_repeated_n_times(result, "所有", 1):
                print(f"出现想要结果:{result}")
                return True
    print(f"未出现想要结果 当前结果：{result}")
    return False


@run_if_enabled
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


@run_if_enabled
def cube_one():
    pyautogui.leftClick(MOUSE_X, MOUSE_Y)  # 单击 再使用一次魔方
    pyautogui.press("enter", 3, 0.02)
    time.sleep(2)


def recognize_text_in_screen_region(ocr, left, top, right, bottom):
    # 捕获屏幕区域图像
    screenshot = pyautogui.screenshot()
    image = np.array(screenshot)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    # 裁剪图像为指定区域
    region_image = image[top:bottom, left:right]
    # 按行截图
    line1 = region_image[0:15, :]
    line2 = region_image[15:30, :]
    line3 = region_image[30:bottom - top, :]
    # 显示图像
    lines = [line1, line2, line3]
    result = []
    # show_image(region_image)
    for line in lines:
        # 进行文字识别
        # show_image(line)
        r = ocr.ocr_for_single_line(line)
        result.append(r.get("text"))
    return result


def show_image(img):
    # 创建窗口并展示图像
    # cv2.namedWindow("img ", cv2.WINDOW_NORMAL)
    cv2.imshow("img", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def auto_cube(ocr, wanna_result: List):
    while True:
        cube_one()
        result = recognize_text_in_screen_region(ocr, LEFT, TOP, RIGHT, BOTTOM)
        if check_result1(result, wanna_result):
            config.enabled = False
        time.sleep(0.5)


def init_hwnd():
    # 根据窗口标题查找窗口句柄
    hwnd = win32gui.FindWindow("MapleStoryClass", "MapleStory")

    if hwnd != 0:
        # 获取外部程序的窗口句柄
        window_handle = pyautogui.getWindowsWithTitle('MapleStory')[0]
        # 找到了窗口句柄，将窗口移动到 (0, 0) 位置
        window_handle.moveTo(0, 0)  # 设置新的窗口位置坐标
        win32gui.SetForegroundWindow(hwnd)
        print("初始化成功！")
    else:
        print("窗口未找到，5秒后继续查找")
        time.sleep(5)
        init_hwnd()


if __name__ == '__main__':
    init_hwnd()
    # 只检测和识别水平文字
    cn_ocr = CnOcr(rec_model_name='densenet_lite_136-fc', det_model_name='db_shufflenet_v2_small',
                   det_more_configs={'rotated_bbox': False})
    listener = Listener()
    listener.start()
    while not listener.ready:
        time.sleep(0.01)
    listener.enabled = True
    wanna_result = [["敏捷", "敏捷", "敏捷"], ["力量", "力量", "力量"], ["智力", "智力", "智力"],
                    ["力量", "力量", "力量"], ["所有", "所有", "所有"]]
    #
    # wanna_result = [["敏捷", "敏捷"], ["力量", "力量"], ["智力", "智力"],
    #                 ["力量", "力量"], ["所有", "所有"]]
    auto_cube(cn_ocr, wanna_result)
    # config.enabled = True
    # t1 = time.time()
    # r = check_result1(result=["敏捷：+7", "所有属性：+4%", "每10级敏捷：+2"],
    #                   wanna_result=[["敏捷", "敏捷", "敏捷"], ["力量", "力量", "力量"], ["智力", "智力", "智力"],
    #                                 ["力量", "力量", "力量"], ["所有", "所有", "所有"]])
    # print(f"r={r}")
    # print(time.time() - t1)
    # auto_cube(cn_ocr, ["敏捷", "力量", "最大血", "智力", "运气", "所有"])
    # check_result("敏捷：+7%;智力:+16;角色每10级敏捷：+1")
