# /usr/env/bin python3
import re
import os.path
import os
import math
from PIL import Image


angle = 10
scale = 1.
pi = 3.1415926


def rotate_bbox(x, y):
    temp_angle = pi * angle / 180
    x1 = float(x)
    y1 = 600 - float(y)
    x2 = 480
    y2 = 600 -300

    x = (x1 - x2) * math.cos(temp_angle) - (y1 - y2) * math.sin(temp_angle) + x2
    y = (x1 - x2) * math.sin(temp_angle) + (y1 - y2) * math.cos(temp_angle) + y2
    x = x + 1
    y = 600 - y + 1

    rotated_x = int(x)
    rotated_y = int(y)
    return rotated_x, rotated_y


def transfer_array(billiards_array):
    #0(361,191);3(178,112);8(402,166);9(148,155);10(81,496);11(621,212);15(527,478);
    billiards = billiards_array.rstrip().split(";")
    newbilliards = ''
    for billiard in billiards:
        if billiard.strip() != '':
            #获取category_id
            temp = re.split("[(,!)]", billiard)
            catetory_id, x, y = temp[0], temp[1], temp[2]
            rotated_x, rotated_y = rotate_bbox(x, y)
            newbilliards = newbilliards + catetory_id + '(' + str(rotated_x) + ',' + str(rotated_y) + ');'
    return newbilliards

def transfer_process(label_file,  dst_rec_dir):
    '''将label文件的坐标转换后保存'''

    file_object = open(label_file, 'r')
    label_rotation = os.path.join(dst_rec_dir, 'revised.txt')
    fo = open(label_rotation, "w")
    try:
        for line in file_object:
            # print(line.rstrip('\n'))
            # 8 0(361,191);3(178,112);8(402,166);9(148,155);10(81,496);11(621,212);15(527,478); 224960
            billiards_and_picture_name = line.rstrip('\n').split(" ")
            billiards_count = billiards_and_picture_name[0]  #第一个，台球个数
            billiards_array = billiards_and_picture_name[1]  #第二个，台球坐标
            billiards_picture_name = billiards_and_picture_name[2]   #第三个，图片文件名
            billiards = transfer_array(billiards_array)
            contents = billiards_count + ' ' + billiards + ' ' + billiards_picture_name + '\n'
            fo.write(contents)
    finally:
        file_object.close()
        fo.close()


def rotate_process(image_dir, dst_dir):
    '''将图片旋转后保存'''
    filenames = os.listdir(image_dir)
    filenames.sort(key=lambda x: x[:-4])  # 文件夹文件排序

    for file in filenames:
        file_path = os.path.join(image_dir, file)
        # 读取图像
        image = Image.open(file_path)
        """
         对图像进行随机任意角度(0~360度)旋转
        :param mode 邻近插值,双线性插值,双三次B样条插值(default)
        :param image PIL的图像image
        :return: 旋转转之后的图像
        """
        image_rotation = image.rotate(angle, Image.BICUBIC)
        image_rotation.save(os.path.join(dst_dir, file))  # 保存


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
            elif os.path.exists(os.path.join(rec_dir, 'revise.txt')):
                label_file = os.path.join(rec_dir, 'revise.txt')
            else:
                print("revised.txt文件不存在，请查看%s目录" % rec_dir)
                continue

            if not os.path.exists(dst_dir):
                os.makedirs(dst_dir)
            if not os.path.exists(dst_rec_dir):
                os.makedirs(dst_rec_dir)
            rotate_process(image_dir, dst_dir)
            transfer_process(label_file, dst_rec_dir)
            print('转换完成')


def main():
    # 要拷贝数据的根目录
    # root_path = "E:\\coco_bill\\selected-24_object-nodeals"
    source_path = "G:\\dyq\\20200310-Train-rotate"
    dest_path = "G:\\dyq\\20200310-Train-rotation10"
    read_file(source_path, dest_path)


if __name__ == "__main__":
    main()