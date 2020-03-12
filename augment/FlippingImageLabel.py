# /usr/env/bin python3
'''将标注完的数据，进行数据增强
    1、本篇主要是对图像进行翻转
    2、0垂直  1水平 -1水平垂直
    3、对标注的label文件中进行坐标变换
    4、修改第16行的转换方式
'''

import re
import os.path
import os,shutil
from PIL import Image
import cv2

#0垂直  1水平 -1水平垂直
flipping = -1

def transfer_array(billiards_array):
    #0(361,191);3(178,112);8(402,166);9(148,155);10(81,496);11(621,212);15(527,478);
    billiards = billiards_array.rstrip().split(";")
    new_billiards = ''
    for billiard in billiards:
        if billiard.strip() != '':
            #获取category_id
            temp = re.split("[(,!)]", billiard)
            catetory_id, x, y = temp[0], temp[1], temp[2]
            if flipping == 1:
                new_x = 960 - int(x)
                new_y = int(y)
            elif flipping == 0:
                new_x = int(x)
                new_y = 600 - int(y)
            elif flipping == -1:
                new_x = 960 - int(x)
                new_y = 600 - int(y)
            new_billiards = new_billiards + catetory_id + '(' + str(new_x)+',' + str(new_y) + ');'
    return new_billiards


def label_process(label_file,  dst_label_file):
    '''将label文件的拷贝'''
    file_object = open(label_file, 'r')
    fo = open(dst_label_file, "w")
    try:
        for line in file_object:
            # print(line.rstrip('\n'))
            # 8 0(361,191);3(178,112);8(402,166);9(148,155);10(81,496);11(621,212);15(527,478); 224960
            billiards_and_picture_name = line.rstrip('\n').split(" ")
            billiards_count = billiards_and_picture_name[0]  # 第一个，台球个数
            billiards_array = billiards_and_picture_name[1]  # 第二个，台球坐标
            billiards_picture_name = billiards_and_picture_name[2]  # 第三个，图片文件名
            billiards = transfer_array(billiards_array)
            contents = billiards_count + ' ' + billiards + ' ' + billiards_picture_name +'\n'
            fo.write(contents)
    finally:
        file_object.close()
        fo.close()


def flipping_process(image_dir, dst_dir):
    '''将图片旋转后保存'''
    filenames = os.listdir(image_dir)
    filenames.sort(key=lambda x: x[:-4])  # 文件夹文件排序

    for file in filenames:
        file_path = os.path.join(image_dir, file)
        # 读取图像
        image = cv2.imread(file_path)
        if flipping == 1:
            h_flip = cv2.flip(image, 1)
        elif flipping == 0:
            h_flip = cv2.flip(image, 0)
        elif flipping == -1:
            h_flip = cv2.flip(image, -1)

        cv2.imwrite(os.path.join(dst_dir, file), h_flip)


def read_file(source_path, dest_path):
    ''' 自动找到1目录作为图片目录去执行，进行亮度操作后保存到dest_path里
    '''
    source_path.rstrip('/')
    root_dir_name = source_path.split('/')[-1]

    for dirpath, dirnames, filenames in os.walk(source_path):
        if '1' in dirnames:
            image_dir = os.path.join(dirpath, '1')
            dst_dir = image_dir.replace(root_dir_name, dest_path, 1)
            rec_dir = os.path.join(dirpath, 'rec')
            dst_rec_dir = rec_dir.replace(root_dir_name, dest_path, 1)

            if os.path.exists(os.path.join(rec_dir, 'revised.txt')):
                label_file = os.path.join(rec_dir, 'revised.txt')
                dst_label_file = os.path.join(dst_rec_dir, 'revised.txt')
            elif os.path.exists(os.path.join(rec_dir, 'revise.txt')):
                label_file = os.path.join(rec_dir, 'revise.txt')
                dst_label_file = os.path.join(dst_rec_dir, 'revise.txt')
            else:
                print("revised.txt文件不存在，请查看%s目录" % rec_dir)
                continue

            if not os.path.exists(dst_dir):
                os.makedirs(dst_dir)
            if not os.path.exists(dst_rec_dir):
                os.makedirs(dst_rec_dir)
            print(image_dir)
            print(dst_dir)
            print(dst_rec_dir)
            flipping_process(image_dir, dst_dir)
            if(not label_process(label_file, dst_label_file)):
                print("%s文件没有拷贝成功" % label_file)
            print('处理完成')


def main():
    # 要拷贝数据的根目录
    # root_path = "E:\\coco_bill\\selected-24_object-nodeals"
    source_path = "G:\\dyq\\20200310-Train-darken"
    dest_path = "G:\\dyq\\20200310-Train-dou"
    read_file(source_path, dest_path)


if __name__ == "__main__":
    main()