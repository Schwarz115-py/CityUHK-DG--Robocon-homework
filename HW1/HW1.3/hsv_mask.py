import cv2
import numpy as np
from os import path

def main():
    #加载图片路径
    folder = "./dataset"
    filename = "_cgi-bin_mmwebwx-bin_webwxgetmsgimg__&MsgID=4481391946056171767&skey=@crypt_ab3e93f4_bbea51c995bc3a100fcadfdb46c8bf61&mmweb_appid=wx_webfilehelper.jpeg"
    img_path = path.join(folder, filename)
    #cv2.imread 读取图片
    img_bgr = cv2.imread(img_path)   
    if img_bgr is None:   #检查是否读取成功
        print("Image read failed. ")
        exit(1)
    #cv2.cvtColor 转换为 HSV
    img_hsv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)
    # TODO: 定义红/蓝颜色阈值范围（HSV 上下界）
    #H：色相（由色相环得） S：饱和度 V：亮度
    lower_red_low = np.array([0, 120, 60])
    upper_red_low = np.array([10, 255, 255])
    lower_red_high = np.array([160, 120, 60])
    upper_red_high = np.array([179, 255, 255])
    #红色分为两段
    lower_blue = np.array([90, 120, 60])
    upper_blue = np.array([130, 255, 255])
    # TODO: cv2.inRange 生成二值化掩膜
    mask_low = cv2.inRange(img_hsv, lower_red_low, upper_red_low)
    mask_high = cv2.inRange(img_hsv, lower_red_high, upper_red_high)
    mask_red = cv2.bitwise_or(mask_low, mask_high)   #红色有两段，记得合起来（或关系）

    mask_blue = cv2.inRange(img_hsv, lower_blue, upper_blue)
    # TODO: 统计白色像素点数量，输出占比结果
    h, w = img_hsv.shape[:2]   # 通过shape方法获取图片的宽和高，从而计算像素总数
    total = h * w
    red = cv2.countNonZero(mask_red)   #黑色部分所0，非零部分就是这个颜色占有的白色像素点数目
    blue = cv2.countNonZero(mask_blue)

    red_ratio = round(red / total, 3)
    blue_ratio = round(blue / total, 3)
    if red_ratio > blue_ratio:
        print("Red is bigger. ")
    elif red_ratio < blue_ratio:
        print("Blue is bigger. ")
    else:
        print("They are equal. ")


if __name__ == "__main__":
    main()
