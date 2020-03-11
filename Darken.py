# /usr/env/bin python3

import re
import sys
import os
import os.path
import json
import time
import datetime
import os,shutil
from pathlib import Path
from PIL import Image
from PIL import ImageEnhance

def do_detect_process(image_dir, dst_dir):
    '''将图片降低亮度后保存'''
    filenames = os.listdir(image_dir)
    filenames.sort(key=lambda x: x[:-4])  # 文件夹文件排序

    for file in filenames:
        file_path = os.path.join(image_dir, file)
        # 读取图像
        image = Image.open(file_path)
        # 增强亮度
        enh_bri = ImageEnhance.Brightness(image)
        brightness = 0.7
        image_brightened09 = enh_bri.enhance(brightness)
        image_brightened09.save(os.path.join(dst_dir, file))  # 保存

def read_file(source_path, dest_path):
    ''' 自动找到1目录作为图片目录去执行，进行亮度操作后保存到dest_path里
    '''
    source_path.rstrip('/')
    root_dir_name = source_path.split('/')[-1]

    for dirpath, dirnames, filenames in os.walk(source_path):
        if '1' in dirnames:
            image_dir = os.path.join(dirpath, '1')
            dst_dir = image_dir.replace(root_dir_name, dest_path, 1)

            if not os.path.exists(dst_dir):
                os.makedirs(dst_dir)
            print(image_dir)
            print(dst_dir)

            do_detect_process(image_dir, dst_dir)


def main():
    # 要拷贝数据的根目录
    # root_path = "E:\\coco_bill\\selected-24_object-nodeals"
    source_path = "G:\\dyq\\20200310-Train-darken"
    dest_path = "G:\\dyq\\20200310-Train-darken07"
    read_file(source_path, dest_path)


if __name__ == "__main__":
    main()