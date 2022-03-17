import argparse
import cv2

parser = argparse.ArgumentParser()
parser.add_argument('--path', default='./Lena.png', help='Image path.')
parser.add_argument('--out_png', default='./Lena_compressed.png',
                    help='Output image path for lossless result.')
parser.add_argument('--out_jpg', default='./Lena_compressed.jpg',
                    help='Output image path for lossy result.')
params = parser.parse_args()
img = cv2.imread(params.path)

# 낮은 압축률로 이미지를 저장한다. - 파일 크기는 크지만 디코딩이 빠르다
cv2.imwrite(params.out_png, img, [cv2.IMWRITE_PNG_COMPRESSION, 0])

# 이미지를 저장하고 다시 불러들여 원본과 동일한지 비교한다.
saved_img = cv2.imread(params.out_png)
assert saved_img.all() == img.all()

# 이미지를 낮은 화질로 저장한다. - 크기가 더 작아진다.
cv2.imwrite(params.out_jpg, img, [cv2.IMWRITE_JPEG_QUALITY, 0])