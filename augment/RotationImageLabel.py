# /usr/env/bin python3
import re
import os.path
import os, sys
import math
from PIL import Image
import logging
from  utils.date_utils import MyDateUtils

angle = 10
scale = 1.
pi = 3.1415926


def rotate_bbox(x, y):
    temp_angle = pi * angle / 180
    x1 = float(x)
    y1 = 600 - float(y)
    x2 = 480
    y2 = 600 - 300

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

def transfer_process(label_file, dst_rec_dir, dst_dir, timestamp):
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
            billiards_picture_name = str(timestamp)[-4:-1] + '_' + billiards_picture_name
            # logger.info(billiards_picture_name)
            billiards = transfer_array(billiards_array)
            image_file = os.path.join(dst_dir,billiards_picture_name + '.bmp')
            if os.path.exists(image_file):
                contents = billiards_count + ' ' + billiards + ' ' + billiards_picture_name + '\n'
            else:
                logger.error('%s文件不存在，请检查' % image_file)
            fo.write(contents)
    finally:
        file_object.close()
        fo.close()


def rotate_process(image_dir, dst_dir, timestamp):
    '''将图片旋转后保存'''
    filenames = os.listdir(image_dir)
    filenames.sort(key=lambda x: x[:-4])  # 文件夹文件排序

    for file in filenames:
        file_path = os.path.join(image_dir, file)
        # 读取图像
        try:
            image = Image.open(file_path)
            """
             对图像进行随机任意角度(0~360度)旋转
            :param mode 邻近插值,双线性插值,双三次B样条插值(default)
            :param image PIL的图像image
            :return: 旋转转之后的图像
            """
            image_rotation = image.rotate(angle, Image.BICUBIC)
            file = str(timestamp)[-4:-1] + '_' + file
            image_rotation.save(os.path.join(dst_dir, file))  # 保存
        except OSError:
            logger.error('%s转换失败' % file_path)


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
                logger.error("revised.txt文件不存在，请查看%s目录" % rec_dir)
                continue

            if not os.path.exists(dst_dir):
                os.makedirs(dst_dir)
            if not os.path.exists(dst_rec_dir):
                os.makedirs(dst_rec_dir)
            date_string = MyDateUtils.cur_datetime()
            timestamp = str(MyDateUtils.datetime_to_seconds(date_string))
            rotate_process(image_dir, dst_dir,  timestamp)
            transfer_process(label_file, dst_rec_dir, dst_dir, timestamp)
            logger.info('%s目录增强成功' % image_dir)


def main():
    # 要拷贝数据的根目录
    # root_path = "E:\\coco_bill\\selected-24_object-nodeals"
    # source_path = "G:\\dyq\\20200310-Train-rotate"
    # dest_path = "G:\\dyq\\20200310-Train-rotation10"
    source_path = "/home/zealens/dyq/datas/train/20191226-1600-mijiqiu-Train"
    dest_path = "20191226-1600-mijiqiu-Train-rotate"

    read_file(source_path, dest_path)
    logger.info('对%s进行角度转换完成，请查看%s' % (source_path, dest_path))


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(os.path.basename(sys.argv[0]).split(".")[0])
    main()