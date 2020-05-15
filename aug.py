from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw
import cv2
import numpy as np
from math import *
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

def AddNoiseSingleChannel(single):
    diff = 255-single.max()
    noise = np.random.normal(0,1+r(6),single.shape)
    noise = (noise - noise.min())/(noise.max()-noise.min())
    noise= diff*noise
    noise= noise.astype(np.uint8)
    dst = single + noise
    return dst

def addNoise(img,sdev = 0.5,avg=10):
    img[:,:,0] =  AddNoiseSingleChannel(img[:,:,0])
    img[:,:,1] =  AddNoiseSingleChannel(img[:,:,1])
    img[:,:,2] =  AddNoiseSingleChannel(img[:,:,2])
    return img

def r(val):
    return int(np.random.random() * val)

def AddGauss(img, level):
    return cv2.blur(img, (level * 2 + 1, level * 2 + 1))

def AddSmudginess(img, Smu):
    rows = r(Smu.shape[0] - 50)

    cols = r(Smu.shape[1] - 50)
    adder = Smu[rows:rows + 50, cols:cols + 50]
    print(img.shape)
    adder = cv2.resize(adder, (50, 50))
    #   adder = cv2.bitwise_not(adder)
    img = cv2.resize(img,(50,50))
    img = cv2.bitwise_not(img)
    img = cv2.bitwise_and(adder, img)
    img = cv2.bitwise_not(img)
    return img

def find_new_points(points, matrix):
    for index, p in enumerate(points):
        px = (matrix[0][0] * p[0] + matrix[0][1] * p[1] + matrix[0][2]) / ((matrix[2][0] * p[0] + matrix[2][1] * p[1] + matrix[2][2]))
        py = (matrix[1][0] * p[0] + matrix[1][1] * p[1] + matrix[1][2]) / ((matrix[2][0] * p[0] + matrix[2][1] * p[1] + matrix[2][2]))
        points[index] = (int(px), int(py))  # after transformation
    return points

def rot(img,angel,shape,max_angel, points):
    """ 使图像轻微的畸变

        img 输入图像
        factor 畸变的参数
        size 为图片的目标尺寸

    """
    size_o = [shape[1],shape[0]]

    size = (shape[1]+ int(shape[0]*cos((float(max_angel )/180) * 3.14)),shape[0])


    interval = abs( int( sin((float(angel) /180) * 3.14)* shape[0]))

    pts1 = np.float32([[0,0]         ,[0,size_o[1]],[size_o[0],0],[size_o[0],size_o[1]]])
    if(angel>0):

        pts2 = np.float32([[interval,0],[0,size[1]  ],[size[0],0  ],[size[0]-interval,size_o[1]]])
    else:
        pts2 = np.float32([[0,0],[interval,size[1]  ],[size[0]-interval,0  ],[size[0],size_o[1]]])

    M  = cv2.getPerspectiveTransform(pts1,pts2)
    points = find_new_points(points, M)
    dst = cv2.warpPerspective(img,M,size)

    return dst, points

def rotRandrom(img, factor, size, points):
    shape = size
    pts1 = np.float32([[0, 0], [0, shape[0]], [shape[1], 0], [shape[1], shape[0]]])
    pts2 = np.float32([[r(factor), r(factor)], [ r(factor), shape[0] - r(factor)], [shape[1] - r(factor),  r(factor)],
                       [shape[1] - r(factor), shape[0] - r(factor)]])
    M = cv2.getPerspectiveTransform(pts1, pts2)
    points = find_new_points(points, M)
    dst = cv2.warpPerspective(img, M, size)
    return dst, points



def tfactor(img):
    hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)

    hsv[:,:,0] = hsv[:,:,0]*(0.8+ np.random.random()*0.2)
    hsv[:,:,1] = hsv[:,:,1]*(0.3+ np.random.random()*0.7)
    hsv[:,:,2] = hsv[:,:,2]*(0.2+ np.random.random()*0.8)

    img = cv2.cvtColor(hsv,cv2.COLOR_HSV2BGR)
    return img

def random_envirment(img,data_set, points):
    index=r(len(data_set))
    env = cv2.imread(data_set[index])

    env = cv2.resize(env,(img.shape[1],img.shape[0]))
    polygon = Polygon((points[0], points[2], points[3], points[1]))
    for y in range(env.shape[0]): #70
        for x in range(env.shape[1]): #226
            point = Point(x, y)
            if polygon.contains(point):
                env[y,x] = img[y,x]
    # env = cv2.blur(env, (5, 5))
    return env
    # any point within the 4 point figure does not change, belongs to the plate

    # bak = (img==0)
    # bak = bak.astype(np.uint8)*255
    #
    # cv2.imshow('bak',bak)
    # cv2.waitKey(0)
    # inv = cv2.bitwise_and(bak,env)
    # cv2.imshow('inv', inv)
    # cv2.waitKey(0)
    # img = cv2.bitwise_or(inv,img)
    # cv2.imshow('img', img)
    # cv2.waitKey(0)
    # return img