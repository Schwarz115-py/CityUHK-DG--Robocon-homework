import argparse
import os
import cv2


def parse_args():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description="图像批处理脚本")
    parser.add_argument('--dir', type = str, required = True, help = 'The path of the directory')   #添加可选参数--dir，表示文件夹路径
    return parser.parse_args()   #返回解析后命令行参数的实例对象


def main():
    args = parse_args()
    img_list = []
    if not os.path.exists(args.dir):
        print("The path does not exist. ")
        exit(1)   #检查传递的路径是否存在
    if not os.path.isdir(args.dir):
        print("The path is not a directory. ")
        exit(1)   #检查传递的路径是不是一个文件夹
    for dirpath, dirname,files in os.walk(args.dir):   #os.walk():递归遍历文件夹，生成文件路径、子文件夹名、文件名三个列表
        for file in files:
            ext = os.path.splitext(file)[1]   #获取文件后缀名。splitext方法将文件名前段和后缀切分，形成一个元组。            if ext.lower() in (".png", ".jpg"):   #不区分大小写，所以全部后缀改为小写（ext是字符串）
            path = os.path.join(dirpath, file)   #将文件夹路径和文件名拼接起来
            img_list.append(path)
    all_info = []
    for img_path in img_list:
        img_name = os.path.basename(img_path)   #获取图片的文件名，注意不是.name
        image = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)   #读取图片，cv2.IMREAD_UNCHANGED用来读取带四通道的png图片
        if image is None:   #检查图片是否读取成功（一定要做）
            print(f"Image read failed. {img_name}")
            continue
        shape = image.shape   #获取图片的各类参数，得到一个由高、宽、通道数组成的三元组（灰度图两个）
        if len(shape) == 3:
            h, w, c = shape
        else:
            h, w = shape
            c = 1   #额外处理灰度图只有单通道的情况，因为灰度图里shape只有两个元素了
        img_dict = {
            'name' : img_name,
            'resolution' : f"{w} * {h}",   #获取分辨率：宽*高，注意和shape的反了过来
            'channel' : c
        }
        all_info.append(img_dict)
    for info in all_info:
        print(info)


if __name__ == "__main__":   #检测是不是直接运行脚本
    main()