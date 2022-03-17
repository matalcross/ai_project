import numpy
import cv2

def print_capture_properties(*args):
  capture = cv2.VideoCapture(*args)
  print('Created catpture:', ' '.join(map(str, args)))
  print('Frame count:', int(capture.get(cv2.CAP_PROP_FRAME_COUNT)))
  print('Frame width:', int(capture.get(cv2.CAP_PROP_FRAME_WIDTH)))
  print('Frame height:', int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT)))
  print('Frame rate:', capture.get(cv2.CAP_PROP_FPS))

print_capture_properties('./video.mp4')