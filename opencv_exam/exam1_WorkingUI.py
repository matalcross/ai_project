import cv2, numpy as np

cv2.namedWindow('window')

# [0,255] 범위로 청색, 녹색, 적색의 색상 구성 요소 순서로 해석되는 세 개의 값이 배열
fill_val = np.array([255,255,255], np.uint8)

# trackbar_callback함수에서 호출하는 보조 함수를 추가
# 색상 구성 요소 인덱스와 설정될 새 값을 받음
def trackbar_callback(idx, value):
  fill_val[idx] = value
  print("idx = ", idx, ", value = ", value)

# 세개의 탐색 바를 window에 추가하고 파이썬 lambda 함수를 사용해 각 탐색바 콜백을 특정 색상 구성 요소에 바인딩한다.
cv2.createTrackbar('R', 'window', 0, 255, lambda v: trackbar_callback(2, v))
cv2.createTrackbar('G', 'window', 0, 255, lambda v: trackbar_callback(1, v))
cv2.createTrackbar('B', 'window', 0, 255, lambda v: trackbar_callback(0, v))

while True:
  image = np.full((500, 500, 3), fill_val)
  cv2.imshow('window', image)
  key = cv2.waitKey(3)
  if key == 27:
    break;
  
cv2.destoryAllWindow()
