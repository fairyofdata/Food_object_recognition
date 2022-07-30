import cv2
import numpy as np
from PIL import Image
import os

'''
이미지 자동 바운딩 함수(txt 라벨 생성)
'''
def autobounding(img):
  image_gray = cv2.imread(img, cv2.IMREAD_GRAYSCALE)
  blur = cv2.GaussianBlur(image_gray, ksize=(5,5), sigmaX=0)
  edged = cv2.Canny(blur, 10, 250)
  kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7,7))
  closed = cv2.morphologyEx(edged, cv2.MORPH_CLOSE, kernel)
  contours, _ = cv2.findContours(closed.copy(),cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
  contours_xy = np.array(contours)
  contours_xy.shape
  x_min, x_max = 0,0
  value = list()
  for i in range(len(contours_xy)):
      for j in range(len(contours_xy[i])):
          value.append(contours_xy[i][j][0][0])
          x_min = min(value)
          x_max = max(value)
  y_min, y_max = 0,0
  value = list()
  for i in range(len(contours_xy)):
      for j in range(len(contours_xy[i])):
          value.append(contours_xy[i][j][0][1])
          y_min = min(value)
          y_max = max(value)
  image1 = Image.open(img)
  t_x, t_y = image1.size
  x = format(round(((x_max-x_min)/2)/t_x, 6), ".6f")
  y = format(round(((y_max-y_min)/2)/t_y, 6), ".6f")
  w = format(round((x_max-x_min)/t_x, 6), ".6f")
  h = format(round((y_max-y_min)/t_y, 6), ".6f")
  address = str(str(0) + " " + x + " " + y + " " + w + " " + h)
  with open(f"./bounding/{img[img.rfind('/')+1:-4]}.txt",'w') as f:
    f.write(address)
    
'''
이미지 자동 바운딩 함수(폴더 단위 적용)
''' 
def directory_autobounding(directory):
  path = directory + "/"
  file_list = os.listdir(path)
  file_list_txt = [file for file in file_list if file.endswith(".jpg")]
  for file in file_list_txt:
    autobounding(path + file)
    
directory_autobounding("./image")
    
    