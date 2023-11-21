import cv2
import keyboard
import time

import numpy as np
import win32gui
from ppocronnx import TextSystem
from cnocr import CnOcr

from auto_cube import show_image

is_running = True


def toggle_script():
    global is_running
    is_running = not is_running
    if is_running:
        print("脚本已激活")
    else:
        print("脚本已暂停")


def main_script():
    while True:
        if is_running:
            # 在这里编写你的脚本逻辑
            print("脚本正在运行...")
            relative_x, relative_y = get_relative_mouse_position()
            print(f"相对坐标：({relative_x}, {relative_y})")
        time.sleep(1)


# 注册按键监听器，按下F5时切换脚本状态
keyboard.on_press_key("F5", lambda _: toggle_script())
import pyautogui
import pygetwindow as gw


def get_relative_mouse_position():
    # 获取当前鼠标位置
    x, y = pyautogui.position()

    # 获取当前窗口句柄
    handle = pyautogui.getActiveWindow()

    # 获取当前窗口的位置和大小
    window = gw.getWindowsWithTitle(handle.title)[0]
    window_x, window_y, window_width, window_height = window.left, window.top, window.width, window.height

    # 计算相对坐标
    relative_x = x - window_x
    relative_y = y - window_y

    return relative_x, relative_y

    # 示例用法

    # 启动主脚本
    main_script()


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
    # init_hwnd()
    # # main_script()
    # screenshot = pyautogui.screenshot()
    # image = np.array(screenshot)
    # image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    #
    # # 指定裁剪区域的坐标
    # left, top, right, bottom = 608, 463, 774, 508
    #
    # # 裁剪图像为指定区域
    # region_image = image[top:bottom, left:right]
    # line_width = 15
    # # 按行截取图像区域
    # line1 = region_image[0:line_width, :]
    # line2 = region_image[line_width:line_width * 2, :]
    # line3 = region_image[line_width * 2:bottom - top, :]
    # show_image(region_image)
    img_fp = "test3.png"
    ocr = CnOcr(rec_model_name='densenet_lite_136-fc', det_model_name='db_shufflenet_v2_small',
                det_more_configs={'rotated_bbox': False})
    out1 = ocr.ocr_for_single_line(img_fp)
    print(out1)
    img_fp = "test.png"
    out2 = ocr.ocr(img_fp)
    print(out2)
    # lines = [line1, line2, line3]
    # print(text_ocr.detect_and_ocr(region_image))
    # for line in lines:
    #     text = text_ocr.ocr_single_line(line)
    #     show_image(line)
    #     print(text)
    #     print(text[0])
    # # 创建窗口并展示图像
    # cv2.namedWindow("region_image ", cv2.WINDOW_NORMAL)
    # cv2.imshow("region_image", region_image)
    # # 创建窗口并展示图像
    # cv2.namedWindow("Line 1", cv2.WINDOW_NORMAL)
    # cv2.imshow("Line 1", line1)
    #
    # cv2.namedWindow("Line 2", cv2.WINDOW_NORMAL)
    # cv2.imshow("Line 2", line2)
    #
    # cv2.namedWindow("Line 3", cv2.WINDOW_NORMAL)
    # cv2.imshow("Line 3", line3)
    # # 等待按键事件，按下任意键后关闭窗口
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    # 按行截取图像区域
    # line1 = region_image[0:15, :]
    # line2 = region_image[15:30, :]
    # line3 = region_image[30:bottom - top, :]
    # 裁剪图像为指定区域

    # region_image = image.crop((left, top, right, bottom))
    # # 按行截图
    # line1 = region_image.crop((0, 0, right - left, 15))
    # line2 = region_image.crop((0, 15, right - left, 30))
    # line3 = region_image.crop((0, 30, right - left, bottom - top))
    # region_image.show()
    # 显示图像
