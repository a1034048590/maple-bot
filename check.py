import time
import cv2
import mss
import numpy as np
import requests


def show_image(img):
    # 创建窗口并展示图像
    cv2.imshow("img", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def match_template_on_screen(template_image_path, x1, y1, x2, y2, threshold=0.8):
    # 加载待匹配图像
    template_image = cv2.imread(template_image_path, cv2.COLOR_RGBA2RGB)  # 待匹配图像，灰度模式

    # 捕获屏幕区域的图像


    target_image = capture_screen(x1, y1, x2, y2)
    show_image(target_image)

    matching_method = cv2.TM_CCOEFF

    # 执行图像匹配
    result = cv2.matchTemplate(target_image, template_image, matching_method)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    print(min_val)
    # 如果匹配结果小于阈值，则未检测到目标
    if min_val > threshold:
        return False

    return True


MIAO_CODE = 'tvHK4mP'  # string，喵码。指定发出的提醒，一个提醒对应一个喵码。（必填）


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


def check_bag():
    template_image_path = "img.png"
    x1, y1 = 0, 688  # 左上角坐标
    x2, y2 = 175, 723  # 右下角坐标
    is_detected = match_template_on_screen(template_image_path, x1, y1, x2, y2)
    if is_detected:
        print("包未满")
    else:
        print("包已满或者游戏消失")
        miao_tixing("包已满或者游戏消失")


if __name__ == '__main__':
    while True:
        check_bag()
        time.sleep(2)
