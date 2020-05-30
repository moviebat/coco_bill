#!/usr/bin/env/python3

import os
import cv2

'''将新的海康相机+创威镜头照片进行裁切
    1、新图片大小1280*1024
    2、从图片中裁切出1280*800
    3、然后进行等比例缩小成960*600
    4、这样再进行畸变校正
'''


# 按照指定的范围裁切图片并输出
def img_cutter(img_input_path, x, y, w, h, img_output_path):
    img = cv2.imread(img_input_path)
    cropped = img[y:y+h, x:x+w]
    cv2.imwrite(img_output_path, cropped)
    print("cut img: " + img_input_path)

# 将图像缩放到指定宽高，要求源目宽高比相同
def img_resize(img_input_path, w, h, img_output_path):
    img = cv2.imread(img_input_path)
    shrink = cv2.resize(img, (w, h))
    cv2.imwrite(img_output_path, shrink)
    print("resize img: " + img_input_path)

# 整个目录遍历图片进行处理
def img_cut_process(dir_path, x, y, w, h):
    #parent_dir_path = os.path.dirname(dir_path)
    #output_dir_path = os.path.join(parent_dir_path, "output")
    output_dir_path = dir_path + "-output"
    if not os.path.exists(output_dir_path):
        os.mkdir(output_dir_path)

    index = 5
    for img in os.listdir(dir_path):
        # 仅支持bmp，jpg，png
        if not img.endswith(".bmp") and not img.endswith(".png") and not img.endswith(".jpg"):
            continue
        img_new_name = 'frame_{:08d}.bmp'.format(index)
        index += 5
        img_full_path = os.path.join(dir_path, img)
        img_output_path = os.path.join(output_dir_path, img_new_name)
        img_cutter(img_full_path, x, y, w, h, img_output_path)
        img_resize(img_output_path, 960, 600, img_output_path)

    print("finished! output path: " + output_dir_path)

def main():
    img_dir_path = r"F:\0530shibie\calib_yc_zgc_hk_24\table\1"
    img_cut_process(img_dir_path, 0, 100, 1280, 800)

if __name__ == "__main__":
    main()

