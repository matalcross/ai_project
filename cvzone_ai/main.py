import os
import cv2
from cvzone.HandTrackingModule import HandDetector
import numpy as np

# 환경설정
width, height = 1280, 720
folderPath = "ppt"

# 카메라 셋업
cap = cv2.VideoCapture(0)
cap.set(3, width)
cap.set(4, height)

# 이미지 정보를 보여준다.
pathImages = sorted(os.listdir(folderPath))
# print(pathImages)

# 변수
imgNumber = 0
hs, ws = int(120*1), int(213*1)
gestureThreshold = 300
buttonPressed = False
buttonCounter = 0
buttonDelay = 30
annotations = [[]]
annotationNumber = 0
annotationStart = False

# 손동작 감지
detector = HandDetector(detectionCon=0.8, maxHands=1)

while True:
    # 이미지 이력하기
    success, img = cap.read()
    img = cv2.flip(img, 1)

    pathFullImage = os.path.join(folderPath, pathImages[imgNumber])
    imgCurrent_o = cv2.imread(pathFullImage)
    imgCurrent = cv2.resize(imgCurrent_o, (width, height))

    # hands, img = detector.findHands(img, flipType=False)
    hands, img = detector.findHands(img)
    cv2.line(img, (0, gestureThreshold), (width, gestureThreshold), (255,0,0), 10)

    print(annotationNumber)

    if hands and buttonPressed is False:
        hand = hands[0]
        fingers = detector.fingersUp(hand)

        # 손의 중앙값을 찾는다.
        cx, cy = hand['center']
        # print(fingers)

        lmList = hand['lmList']

        # 선택된 부분으로 그리기
        # indexFinger = lmList[8][0], lmList[8][1]
        xVal = int(np.interp(lmList[8][0], [width // 2, w],[0, width]))
        yVal = int(np.interp(lmList[8][1], [150, height-150], [0, height]))
        indexFinger = xVal, yVal

        print(indexFinger)

        if cy <= gestureThreshold:
            annotationStart = False

            # 왼손 엄지를 인식하였을경우
            if fingers == [1,0,0,0,0]:
                annotationStart = False
                print("Left")
                if imgNumber > 0 :
                    annotations = [[]]
                    annotationNumber = 0
                    buttonPressed = True
                    imgNumber -= 1

            # 왼손 마지막손가락를 인식하였을경우
            if fingers == [0,0,0,0,1]:
                annotationStart = False
                print("Right")
                if imgNumber < len(pathImages)-1:
                    annotations = [[]]
                    annotationNumber = 0
                    buttonPressed = True
                    imgNumber += 1

            # 드로잉 정보 삭제하기
            if fingers == [0, 1, 1, 1, 0]:
                if annotations:
                    if annotationNumber > 0:
                        annotations.pop(-1)
                        annotationNumber -= 1
                        buttonPressed = True

        # 포인터로 사용
        if fingers == [0, 1, 1, 0, 0]:
            print("Point")
            cv2.circle(imgCurrent, indexFinger, 12, (0,0,255), cv2.FILLED)
            annotationStart = False

        # 포인트 그리기
        if fingers == [0, 1, 0, 0, 0]:
            print("Drawing")
            if annotationStart is False:
                annotationStart = True
                annotationNumber += 1
                annotations.append([])
            cv2.circle(imgCurrent, indexFinger, 12, (0,0,255), cv2.FILLED)
            annotations[annotationNumber].append(indexFinger)
        else:
            annotationStart = False
    else:
        annotationStart = False

    # 만약 버턴이 동작된것이라면 초기화
    if buttonPressed:
        buttonCounter += 1
        if buttonCounter > buttonDelay:
            buttonCounter = 0
            buttonPressed = False

    for i in range(len(annotations)):
        for j in range(len(annotations[i])):
            if j != 0:
                cv2.line(imgCurrent, annotations[i][j - 1], annotations[i][j], (0,0,200), 12)

    # 웹카메라 이미지를 슬라이스여 추가
    imgSmall = cv2.resize(img, (ws, hs))
    h, w, _ = imgCurrent.shape
    imgCurrent[0:hs, w-ws:w] = imgSmall

    cv2.imshow("Images", img)
    cv2.imshow("Slides", imgCurrent)
    key = cv2.waitKey(1)

    if key == ord('q'):
        break
