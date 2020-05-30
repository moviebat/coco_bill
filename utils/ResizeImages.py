import cv2 as cv
import os.path
import os,sys
import logging
from PIL import Image

'''海康200万相机采集1920*1200图片，自动将图片缩小到1/4大小，即长宽均相应缩小一半
'''


def resize_images(source_path, dest_path):
    ''' 自动找到1目录作为图片目录去执行，进行resize操作后保存到dest_path里
    '''
    source_path.rstrip('/')
    root_dir_name = source_path.split('/')[-1]

    for dirpath, dirnames, filenames in os.walk(source_path):
        if '1' in dirnames:
            image_dir = os.path.join(dirpath, '1')
            dst_dir = os.path.join(dest_path, '1')

            if not os.path.exists(dst_dir):
                os.makedirs(dst_dir)

            filenames = os.listdir(image_dir)
            filenames.sort(key=lambda x: x[:-4])  # 文件夹文件排序

            for file in filenames:
                file_path = os.path.join(image_dir, file)
                # 读取图像
                try:
                    image = cv.imread(file_path)
                    # 打印出图片尺寸
                    # 将图片高和宽分别赋值给x，y
                    height, width = image.shape[:2]

                    # 缩小图片
                    size = (int(width * 0.5), int(height * 0.5))
                    new_image = cv.resize(image, size, interpolation=cv.INTER_AREA)
                    #cv.imshow("缩小", new_image)
                    cv.imwrite(os.path.join(dst_dir, file), new_image)
                except OSError:
                    logger.error('%s图片resize失败' % file_path)
                logger.info('对%s进行图片resize成功' % image_dir )


def main():
    source_path = "F:\\0530shibie\\baiqiu"
    dest_path = "F:\\0530shibie\\baiqiu_resized"
    resize_images(source_path, dest_path)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(os.path.basename(sys.argv[0]).split(".")[0])
    main()


