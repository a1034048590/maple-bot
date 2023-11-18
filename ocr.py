from typing import List

import cv2
import numpy as np
import pyautogui

from cnocr import CnOcr
import time
import win32gui

def is_repeated_n_times(string, char, n):
    count = string.count(char)
    return count == n


def check_result(result, wanna_result=None, same_line=2):
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


def cube_one(cn_ocr):
    pyautogui.leftClick(389, 458)  # 单击
    pyautogui.press("enter", 3, 0.02)
    result_l, result_t, result_r, result_b = 324, 373, 491, 416
    time.sleep(2)
    return recognize_text_in_screen_region(cn_ocr, result_l, result_t, result_r, result_b);


def recognize_text_in_screen_region(cn_ocr, left, top, right, bottom):
    # 捕获屏幕区域图像
    screenshot = pyautogui.screenshot()
    image = np.array(screenshot)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    # 裁剪图像为指定区域
    region_image = image[top:bottom, left:right]

    # 进行文字识别
    text = cn_ocr.ocr(region_image)
    result = ''
    for t in text:
        result += t.get('text') + ';'
    return result


def auto_cube(cn_ocr: CnOcr, wanna_result: List, same_line):
    while True:
        if check_result(cube_one(cn_ocr), wanna_result, same_line):
            exit()
        time.sleep(2)


def init_hwnd():
    # 获取外部程序的窗口句柄
    window_handle = pyautogui.getWindowsWithTitle('MapleStory')[0]

    # 移动窗口到指定位置
    # 根据窗口标题查找窗口句柄
    hwnd = win32gui.FindWindow("MapleStoryClass", "MapleStory")

    if hwnd != 0:
        # 找到了窗口句柄，将窗口移动到 (0, 0) 位置
        window_handle.moveTo(0, 0)  # 设置新的窗口位置坐标
        win32gui.SetForegroundWindow(hwnd)
        print("初始化成功！")
    else:
        print("窗口未找到，5秒后继续查找")
        time.sleep(5)
        init_hwnd()


if __name__ == '__main__':
    # DEBUG 力量无法识别 ->力里
    ocr = CnOcr()
    init_hwnd()
    auto_cube(ocr, ["敏捷", "力量", "最大血", "智力", "运气", "所有"], 3)
    # check_result("敏捷：+7%;智力:+16;角色每10级敏捷：+1")
