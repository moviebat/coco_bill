# /usr/env/bin python3
'''将标注完的数据，生成COCO数据格式的训练数据train
    1、拷贝图片到train2017目录
    2、读取points文件，进行坐标转换
    3、生成train2017.json文件
    4、
'''

import re
import sys
import os
import os.path
import json
import time
import datetime
import os,shutil
from pathlib import Path


class Info:
    description = ""
    url = ""
    version = "3.0"
    year = 2020
    contributor = "Dengyq"
    date_created = ""

    def __init__(self, description, url, version, year, contributor, date_created):
        self.description = description
        self.url = url
        self.version = version
        self.year = year
        self.contributor = contributor
        self.date_created = date_created

    def __repr__(self):
        return repr((self.description, self.url, self.age, self.version, self.year,
                     self.contributor, self.date_created))


class Image:
    file_name = ''
    width = 960
    height = 600
    id = 0

    def __init__(self, file_name, width, height, id):
        self.file_name = file_name
        self.width = width
        self.height = height
        self.id = id

    def __repr__(self):
        return repr((self.file_name, self.width, self.height, self.id))


class Annotation:
    def __init__(self, area, iscrowd, image_id, bbox, category_id, id):
        self.area = area
        self.iscrowd = iscrowd
        self.image_id = image_id
        self.bbox= bbox
        self.category_id = category_id
        self.id = id

    def __repr__(self):
        return repr((self.area, self.iscrowd, self.image_id, self.bbox, self.category_id, self.id))


class Category:
    def __init__(self, supercategory, id, name):
        self.supercategory = supercategory
        self.id = id
        self.name = name

    def __repr__(self):
        return repr((self.supercategory, self.id, self.name))


class Instance:
    def __init__(self, info, images, annotations, categories):
        self.info = info
        self.images = images
        self.annotations = annotations
        self.categories = categories

    def __repr__(self):
        return repr((self.info, self.images, self.annotations, self.categories))


def create_info():
    date = time.localtime()
    detestr = time.strftime("%Y-%m-%d", date)
    info = Info("IRIP billball coco style Dataset", "none", "3.0", 2019, "Dengyq", detestr)
    return info


def create_images_annotations(picture_name, billiards, image_index, annotation_index):
    images = list()
    annotations = list()
    image = Image('frame_' + picture_name + '.bmp', 960, 600, image_index + 1)
    images.append(image)
    for billiard in billiards:
        if billiard.strip() != '':
            #获取category_id
            temp = re.split("[(,!)]", billiard)
            catetory_id, x, y = temp[0], temp[1], temp[2]
            bbox = [int(x)-10, int(y)-10, 20, 20]
            annotation = Annotation(314, 0, image_index + 1, bbox, int(catetory_id)+1,
                                    annotation_index + 1)
            annotations.append(annotation)
        annotation_index = annotation_index + 1
    return images, annotations


def create_categories():
    categories = [0 for _ in range(16)]
    for index in range(16):
        category = Category(str(index), index+1, str(index))
        categories[index] = category
    return categories


def copy_image(image_dir, train_path, picture_name):
    srcPath = os.path.join(image_dir, 'frame_' + picture_name + '.bmp')
    destPath = os.path.join(train_path, 'frame_' + picture_name + '.bmp')
    if move_file(srcPath, destPath):
        return True
    else:
        return False


def get_billiards(billiards_array):
    #0(361,191);3(178,112);8(402,166);9(148,155);10(81,496);11(621,212);15(527,478);
    billiards = billiards_array.rstrip().split(";")
    return billiards


def do_process(image_dir, label_file, train_path, image_index, annotation_index):
    '''深度方案执行一个目录下图片的识别，图片是已经矫正后的图片'''
    # print("image_dir: %s\npoints_file: %s" % (image_dir, label_file))
    image_list = list()
    annotation_list = list()

    file_object = open(label_file, 'r')
    try:
        for line in file_object:
            #print(line.rstrip('\n'))
            # 8 0(361,191);3(178,112);8(402,166);9(148,155);10(81,496);11(621,212);15(527,478); 224960
            billiards_and_picture_name = line.rstrip('\n').split(" ")
            billiards_array = billiards_and_picture_name[1]
            print(billiards_and_picture_name[2])
            picture_name = regular_filename(str(billiards_and_picture_name[2]))


            billiards = get_billiards(billiards_array)
            image = list()
            annotation = list()
            image, annotation = create_images_annotations(picture_name, billiards,
                                                                    image_index, annotation_index)
            image_list.extend(image)
            image_index = image_index + 1
            annotation_list.extend(annotation)
            annotation_index = annotation_index + len(annotation)
            # print(annotation_list)
            #开始拷贝图片
            # if not copy_image(image_dir, train_path, picture_name):
            #     print("%s文件没有拷贝成功" % picture_name)
    finally:
        file_object.close()
    return image_list, annotation_list


def read_file(root_path, json_file, train_path):
    ''' 自动找到1目录作为图片目录去执行，points文件从同级别rec目录下的revised.txt读取
    '''
    info = create_info()
    image_index = 0
    annotation_index = 0
    image_list = list()
    annotation_list = list()
    for dirpath, dirnames, filenames in os.walk(root_path):
        if '1' in dirnames:
            image_dir = os.path.join(dirpath, '1')
            rec_dir = os.path.join(dirpath, 'rec')
            if os.path.exists(os.path.join(rec_dir, 'revised.txt')):
                label_file = os.path.join(rec_dir, 'revised.txt')
            elif os.path.exists(os.path.join(rec_dir, 'revise.txt')):
                label_file = os.path.join(rec_dir, 'revise.txt')
            else:
                print("revised.txt文件不存在，请查看%s目录" % rec_dir)
                continue

            '''遍历score文件和1目录
            '''
            image, annotation = do_process(image_dir, label_file, train_path,
                                   image_index, annotation_index)
            image_list.extend(image)
            annotation_list.extend(annotation)
            image_index = image_index + len(image)
            annotation_index = annotation_index + len(annotation)

    categories = create_categories()
    content = Instance(info, image_list, annotation_list, categories)
    content_str = json.dumps(content, default=lambda o: o.__dict__, sort_keys=False, indent=4)
    with open(json_file, 'w')as f:
        f.write(content_str)


def regular_filename(filename):
    regular_file_name = filename
    if len(filename) < 8:
        regular_file_name = filename.zfill(8)
    # print(regular_fileName)
    return regular_file_name


def move_file(srcfile, dstfile):
    result = False
    if os.path.isfile(srcfile):
        fpath, fname=os.path.split(dstfile)    #分离文件名和路径
        if not os.path.exists(fpath):
            os.makedirs(fpath)                #创建路径
        # shutil.move(srcfile, dstfile)       #移动文件
        shutil.copyfile(srcfile, dstfile)
        result = True
    return result


def main():
    # root_path = "/home/zealens/1210model"
    # root_path = "/media/zealens/4/dyq/20200203-higherrorrate"
    # 要拷贝数据的根目录
    # root_path = "/home/zealens/dyq/datas/train"
    # json_file = '/home/zealens/dyq/CenterNet/data/coco_bill/annotations/instances_train2017.json'
    # train_path = '/home/zealens/dyq/CenterNet/data/coco_bill/train2017'

    root_path = "E:\\coco_bill\\20200203-mijiqiu"
    #
    json_file = 'E:\\coco_bill\\data\\coco_bill\\annotations\\instances_train2017.json'
    train_path = 'E:\\coco_bill\\data\\coco_bill\\train2017'

    if not os.path.exists(train_path):
        os.makedirs(train_path)  # 创建路径

    fpath, fname = os.path.split(json_file)  # 分离文件名和路径
    if not os.path.exists(fpath):
        os.makedirs(fpath)  # 创建路径

    read_file(root_path, json_file, train_path)


if __name__ == "__main__":
    main()