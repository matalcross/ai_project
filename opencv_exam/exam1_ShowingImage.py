import argparse
import cv2

orig = cv2.imread('./Lena.png')
orig_size = orig.shape[0:2]

print("X = ", orig_size[0], ", Y = ", orig_size[1])

cv2.imshow('Original image', orig)
cv2.waitKey(122000)
