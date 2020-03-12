# /usr/env/bin python3
'''将标注完的数据，进行数据增强
    1、本篇主要是对图像进行亮度降低
    2、直接拷贝标注的label文件
    3、修改15行的数值，即可以进行亮度的增减，
    4、大于1是变量，小于1是变暗
'''


import os.path
import os,shutil
from PIL import Image
from PIL import ImageEnhance

brightness = 0.9


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


def label_process(label_file,  dst_label_file):
    '''将label文件的拷贝'''
    if move_file(label_file, dst_label_file):
        return True
    else:
        return False


def darken_process(image_dir, dst_dir):
    '''将图片旋转后保存'''
    filenames = os.listdir(image_dir)
    filenames.sort(key=lambda x: x[:-4])  # 文件夹文件排序

    for file in filenames:
        file_path = os.path.join(image_dir, file)
        # 读取图像
        image = Image.open(file_path)
        # 增强亮度
        enh_bri = ImageEnhance.Brightness(image)
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
            darken_process(image_dir, dst_dir)
            if(not label_process(label_file, dst_label_file)):
                print("%s文件没有拷贝成功" % label_file)
            print('处理完成')


def main():
    # 要拷贝数据的根目录
    # root_path = "E:\\coco_bill\\selected-24_object-nodeals"
    source_path = "G:\\dyq\\20200310-Train-darken"
    dest_path = "G:\\dyq\\20200310-Train-darken06"
    read_file(source_path, dest_path)


if __name__ == "__main__":
    main()