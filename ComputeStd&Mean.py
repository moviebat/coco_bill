import numpy as np
import cv2
import random
import os
# calculate means and std
from tqdm import tqdm
import numpy as np


def main():
    # root_path = "/home/zealens/1210model"
    filepath = 'E:\\coco_bill\\coco\\train2017'
    # 数据集目录
    pathDir = os.listdir(filepath)

    CNum = 272  # select images 取前10000张图片作为计算样本

    img_h, img_w = 600, 960
    imgs = np.zeros([img_w, img_h, 3, 1])
    means, stdevs = [], []

    i = 0
    for item in pathDir:
        img_path = os.path.join(filepath, item)
        img = cv2.imread(img_path)
        img = cv2.resize(img, (img_h, img_w))  # 将图片进行裁剪[32,32]
        img = img[:, :, :, np.newaxis]
        imgs = np.concatenate((imgs, img), axis=3)
        print(i)
        i = i + 1
    imgs = imgs.astype(np.float32) / 255.

    for i in tqdm(range(3)):
        pixels = imgs[:, :, i, :].ravel()  # flatten
        means.append(np.mean(pixels))
        stdevs.append(np.std(pixels))

    # cv2 : BGR
    means.reverse()  # BGR --> RGB
    stdevs.reverse()

    print("normMean = {}".format(means))
    print("normStd = {}".format(stdevs))
    print('transforms.Normalize(normMean = {}, normStd = {})'.format(means, stdevs))


if __name__ == "__main__":
    main()