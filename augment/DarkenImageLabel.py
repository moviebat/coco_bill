# /usr/env/bin python3
'''将标注完的数据，进行数据增强
    1、本篇主要是对图像进行亮度降低
    2、直接拷贝标注的label文件
    3、修改15行的数值，即可以进行亮度的增减，
    4、大于1是变量，小于1是变暗
'''


import os.path
import os,sys
from PIL import Image
from PIL import ImageEnhance
import logging
from utils.date_utils import MyDateUtils

brightness = 0.9


def transfer_process(label_file, dst_label_file, timestamp):
    '''将label文件的坐标转换后保存'''
    file_object = open(label_file, 'r')
    fo = open(dst_label_file, "w")
    try:
        for line in file_object:
            # 8 0(361,191);3(178,112);8(402,166);9(148,155);10(81,496);11(621,212);15(527,478); 224960
            billiards_and_picture_name = line.rstrip('\n').split(" ")
            billiards_count = billiards_and_picture_name[0]  #第一个，台球个数
            billiards_array = billiards_and_picture_name[1]  #第二个，台球坐标
            billiards_picture_name = billiards_and_picture_name[2]   #第三个，图片文件名
            billiards_picture_name = str(timestamp)[-4:-1] + '_' + billiards_picture_name
            # logger.info(billiards_picture_name)
            contents = billiards_count + ' ' + billiards_array + ' ' + billiards_picture_name + '\n'
            fo.write(contents)
    finally:
        file_object.close()
        fo.close()


def darken_process(image_dir, dst_dir, timestamp):
    '''将图片旋转后保存'''
    filenames = os.listdir(image_dir)
    filenames.sort(key=lambda x: x[:-4])  # 文件夹文件排序

    for file in filenames:
        file_path = os.path.join(image_dir, file)
        # 读取图像
        try:
            image = Image.open(file_path)
            # 增强亮度
            enh_bri = ImageEnhance.Brightness(image)
            image_brightened = enh_bri.enhance(brightness)
            file = str(timestamp)[-4:-1] + '_' + file
            image_brightened.save(os.path.join(dst_dir, file))  # 保存
        except OSError:
            logger.error('%s打开失败' % file_path)


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

            date_string = MyDateUtils.cur_datetime()
            timestamp = str(MyDateUtils.datetime_to_seconds(date_string))
            darken_process(image_dir, dst_dir, timestamp)
            transfer_process(label_file, dst_label_file, timestamp)
            logger.info('对%s进行数据增强成功' % image_dir )
            # if(not label_process(label_file, dst_label_file)):
            #     print("%s文件没有拷贝成功" % label_file)


def main():
    # 要拷贝数据的根目录
    # root_path = "E:\\coco_bill\\selected-24_object-nodeals"
    # source_path = "G:\\dyq\\20200310-Train-darken"
    # dest_path = "G:\\dyq\\20200310-Train-darken06"
    source_path = "/home/zealens/dyq/datas/train/20191018-5000Train"
    dest_path = "20191018-5000Train-darken"

    read_file(source_path, dest_path)
    logger.info('处理完成')


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(os.path.basename(sys.argv[0]).split(".")[0])
    main()