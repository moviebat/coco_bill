import re
import sys
import os
import os.path
import json
import time
import datetime
import os,shutil
from pathlib import Path
import logging


def process_filename(filename):
    regular_file_name = filename
    if len(filename) < 8:
        regular_file_name = filename.zfill(8)
    # print(regular_fileName)
    return regular_file_name


def do_process(image_dir, label_file, new_label_file):
    '''深度方案执行一个目录下图片的识别，图片是已经矫正后的图片'''
    file_object = open(label_file, 'r')
    new_content =''
    success_count = 0
    failure_count = 0
    try:
        for line in file_object:
            #print(line.rstrip('\n'))
            # 8 0(361,191);3(178,112);8(402,166);9(148,155);10(81,496);11(621,212);15(527,478); 224960
            billiards_and_picture_name = line.rstrip('\n').split(" ")
            billiards_count = billiards_and_picture_name[0]  #第一个，台球个数
            billiards_array = billiards_and_picture_name[1]  #第二个，台球坐标
            billiards_picture_name = billiards_and_picture_name[2]   #第三个，图片文件名
            picture_name = 'frame_' + process_filename(str(billiards_picture_name))

            new_picture_name = os.path.join(image_dir, picture_name + '.bmp')
            my_file = Path(new_picture_name)
            if my_file.exists():# 指定的文件存在
                success_count = success_count + 1
                new_content = new_content + billiards_count + ' ' + billiards_array + ' ' + picture_name + '\n'
            else:
                failure_count = failure_count + 1
                logger.error('%s文件不存在' % my_file)

    finally:
        file_object.close()

    try:
        if new_label_file.strip() == '':
            file_object = open(label_file, 'w')
            logger.info('写文件%s成功' % label_file)
        else:
            file_object = open(new_label_file, 'w')
            logger.info('修改revise.txt并删除旧文件成功%s' % label_file)
            os.remove(label_file)
        file_object.write(new_content)
    finally:
        file_object.close()

    return success_count, failure_count


def  regular_filename(root_path):
    success_count = 0
    failure_count = 0
    new_label_file = ''
    for dirpath, dirnames, filenames in os.walk(root_path):
        if '1' in dirnames:
            image_dir = os.path.join(dirpath, '1')
            rec_dir = os.path.join(dirpath, 'rec')
            if os.path.exists(os.path.join(rec_dir, 'revised.txt')):
                label_file = os.path.join(rec_dir, 'revised.txt')
            elif os.path.exists(os.path.join(rec_dir, 'revise.txt')):
                label_file = os.path.join(rec_dir, 'revise.txt')
                new_label_file = os.path.join(rec_dir, 'revised.txt')
            else:
                logger.info("revised.txt或者revise.txt文件不存在，请查看%s目录" % rec_dir)
                continue
            '''遍历score文件和1目录
            '''
            succ_count, fail_count = do_process(image_dir, label_file, new_label_file)
            success_count = success_count + succ_count
            failure_count = fail_count + fail_count

    return success_count, failure_count


def main():
    # 要拷贝数据的根目录
    root_path = "/home/zealens/dyq/datas/train/20191018-5000Train"
    # root_path = "E:\\coco_bill\\20200203-mijiqiu"

    success_count, failure_count = regular_filename(root_path)
    logger.info('数据转换完成，共完成图片拷贝%d张，失败%d个' % (success_count, failure_count))


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(os.path.basename(sys.argv[0]).split(".")[0])
    main()