#/usr/env/bin python3

import sys
import os,shutil

def moveFile(srcfile,dstfile):
    result = False
    if os.path.isfile(srcfile):
        fpath,fname=os.path.split(dstfile)    #分离文件名和路径
        if not os.path.exists(fpath):
            os.makedirs(fpath)                #创建路径
        shutil.move(srcfile,dstfile)          #移动文件
        result = True
    return result

def do_detect_process(image_dir, dst_dir):
    '''深度方案执行一个目录下图片的识别，图片是已经矫正后的图片'''    
    
    filenames = os.listdir(image_dir)
    filenames.sort(key=lambda x:x[:-4]) # 文件夹文件排序
    selectedPicsCount = 0
    count = 0

    for file in filenames:
        file_path = os.path.join(image_dir, file)
        count = count + 1
        
        if count % 5 ==0:
           selectedPicsCount = selectedPicsCount + 1
           destFilePath = os.path.join(dst_dir, file)
           tmpFilePath, tmpFileName = os.path.split(file_path)
           moveFile(file_path,destFilePath)
    print(selectedPicsCount)

def auto_done(root_path):
    ''' 自动找到1目录作为图片目录去执行，将图片文件移动到新的目标目录下的1文件夹下
    '''
    root_path.rstrip('/')
    root_dir_name = root_path.split('/')[-1]
    new_root_dir_name = root_dir_name + "_selected"

    for dirpath, dirnames, filenames in os.walk(root_path):
        if '1' in dirnames:
            image_dir = os.path.join(dirpath, '1')
            dst_dir = image_dir.replace(root_dir_name, new_root_dir_name, 1)

            if not os.path.exists(dst_dir):
                os.makedirs(dst_dir)
            print(image_dir)
            print(dst_dir)

            do_detect_process(image_dir, dst_dir)

def main():
    root_path = "G:\\dyq\\20200230-Test"
    auto_done(root_path)


if __name__ == "__main__":
    main()