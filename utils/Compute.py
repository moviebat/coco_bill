import cv2, os, argparse
import numpy as np
from tqdm import tqdm

'''根据训练图片路径,计算均值和标准差'''

def main():
    dirs = r'/home/zealens/dyq/CenterNet/data/coco_bill/train2017'  # 修改你自己的图片路径
    #dirs = r'/media/zealens/TX2Data/dyq/datas/train'

    img_file_names = os.listdir(dirs)
    m_list, s_list = [], []
    for img_filename in tqdm(img_file_names):
        img = cv2.imread(dirs + '/' + img_filename)
        img = img / 255.0
        m, s = cv2.meanStdDev(img)
        m_list.append(m.reshape((3,)))
        s_list.append(s.reshape((3,)))
    m_array = np.array(m_list)
    s_array = np.array(s_list)
    m = m_array.mean(axis=0, keepdims=True)
    s = s_array.mean(axis=0, keepdims=True)
    print("mean = ", m[0][::-1])
    print("std = ", s[0][::-1])


if __name__ == '__main__':
    main()
