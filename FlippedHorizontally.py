# encoding:utf-8

import cv2


image = cv2.imread("Original.bmp")

# Flipped Horizontally 水平翻转
h_flip = cv2.flip(image, 1)
cv2.imwrite("FlippedHorizontally.bmp", h_flip)

# Flipped Vertically 垂直翻转
v_flip = cv2.flip(image, 0)
cv2.imwrite("FlippedVertically.bmp", v_flip)

# Flipped Horizontally & Vertically 水平垂直翻转
hv_flip = cv2.flip(image, -1)
cv2.imwrite("Double.jpg", hv_flip)