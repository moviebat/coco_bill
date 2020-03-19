import re
import sys
import os
import os.path
import json
import time
import os,shutil
from pathlib import Path
import logging

'''检查标签和图片文件是否对应'''

def check_image_label(image_dir, label_file):
    '''根据label文件，检查图片文件是否存在'''
    file_object = open(label_file, 'r')
    success_count = 0
    failure_count = 0
    try:
        for line in file_object:
            billiards_and_picture_name = line.rstrip('\n').split(" ")
            billiards_picture_name = billiards_and_picture_name[2]   #第三个，图片文件名
            picture_name = os.path.join(image_dir, billiards_picture_name + '.bmp')
            my_file = Path(picture_name)
            if not my_file.exists():# 指定的文件存在
                failure_count = failure_count + 1
                logger.error('%s文件不存在' % my_file)
            else:
                success_count = success_count + 1
    finally:
        file_object.close()

    return success_count, failure_count


def  check_filename(root_path):
    # 0为directory_count，1为directory_succ_count，2为directory_fail_count,3为success_count，4为failure_count
    result = [0,0,0,0,0]
    success_count, failure_count, directory_count, directory_succ_count, directory_fail_count  = 0, 0, 0, 0, 0
    new_label_file = ''
    for dirpath, dirnames, filenames in os.walk(root_path):
        if '1' in dirnames:
            image_dir = os.path.join(dirpath, '1')
            rec_dir = os.path.join(dirpath, 'rec')
            directory_count = directory_count +1
            if not os.path.exists(os.path.join(rec_dir, 'revised.txt')):
                logger.info("revised.txt或者revise.txt文件不存在，请查看%s目录" % rec_dir)
                directory_fail_count + directory_fail_count + 1
                continue
            else: #遍历score文件和1目录
                label_file = os.path.join(rec_dir, 'revised.txt')
                succ_count, fail_count = check_image_label(image_dir, label_file)
                success_count = success_count + succ_count
                failure_count = failure_count + fail_count
                directory_succ_count = directory_succ_count + 1
    result =  directory_count, directory_succ_count, directory_fail_count, success_count, failure_count
    return result


def main():
    # 要拷贝数据的根目录
    #root_path = "/home/zealens/dyq/datas/train1/"
    root_path = "/media/zealens/TX2Data/dyq/datas/train/20200314-1000-Train"
    # root_path = "E:\\coco_bill\\20200203-mijiqiu"

    result = check_filename(root_path)
    logger.info('数据检查完成，共完成%d个目录，成功%d个，失败%d个' % (result[0], result[1], result[2]))
    logger.info('共完成图片检查%d张，失败%d个' % (result[3], result[4]))


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(os.path.basename(sys.argv[0]).split(".")[0])
    main()