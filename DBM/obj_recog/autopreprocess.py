import cv2
import numpy as np
from PIL import Image
import os

def operate_autobounding(img):
    '''
        단일객체 이미지의 바운딩 작업 자동화 함수
        :params
            img : 바운딩 작업을 할 단일 객체 이미지(directory_path + file)
        :action
            바운딩 주소 txt 파일 저장
    '''
    #테두리 검출을 위한 색변환
    image_gray = cv2.imread(img, cv2.IMREAD_GRAYSCALE)
    blur = cv2.GaussianBlur(image_gray, ksize=(5,5), sigmaX=0)
    edged = cv2.Canny(blur, 10, 250)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7,7))
    closed = cv2.morphologyEx(edged, cv2.MORPH_CLOSE, kernel)
    contours, _ = cv2.findContours(closed.copy(),cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    #변환 이미지의 테두리 위치 찾기
    contours_xy = np.array(contours)
    contours_xy.shape
    
    #x 좌표
    x_min, x_max = 0,0
    value = list()
    for i in range(len(contours_xy)):
        for j in range(len(contours_xy[i])):
            value.append(contours_xy[i][j][0][0])
            x_min = min(value)
            x_max = max(value)
    
    #y 좌표
    y_min, y_max = 0,0
    value = list()
    for i in range(len(contours_xy)):
        for j in range(len(contours_xy[i])):
            value.append(contours_xy[i][j][0][1])
            y_min = min(value)
            y_max = max(value)
    
    #추출 좌표 라벨링 형식에 맞게 txt 파일로 저장
    #고유번호, x 중앙값, y 중앙값, 높이, 너비 //전체 길이 1 기준으로의 비율
    image1 = Image.open(img)
    t_x, t_y = image1.size
    x = format(round(((x_max-x_min)/2)/t_x, 6), ".6f")
    y = format(round(((y_max-y_min)/2)/t_y, 6), ".6f")
    w = format(round((x_max-x_min)/t_x, 6), ".6f")
    h = format(round((y_max-y_min)/t_y, 6), ".6f")
    
    address = str(str(0) + " " + x + " " + y + " " + w + " " + h)
    with open(f"./bounding/{img[img.rfind('/')+1:-4]}.txt",'w') as f:
        f.write(address)

def operate_autobounding_directory(img_directory):
    '''
        이미지 바운딩 작업 자동화 함수(폴더 단위 적용)
        :params
            img_directory : 바운딩 작업이 필요한 이미지를 포함한 디렉토리((directory_path / 동일 객체 이미지)
        :action
            디렉토리 단위로 바운딩 주소 txt 파일 저장
    ''' 
    directory_path = img_directory + "/"
    file_list = os.listdir(directory_path)
    file_list_txt = [file for file in file_list if file.endswith(".jpg")]
    for file in file_list_txt:
        operate_autobounding(directory_path + file)
    
operate_autobounding_directory("./image")
    
    