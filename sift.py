# -*- coding: utf-8 -*-
"""
Created on Wed Aug 14 22:59:57 2019

@author: Acer
"""

import cv2
import numpy as np
import os
import math
import itertools

path = 'D://university//aircraft_project//malasongjinshan1//'
all_pic = 167


def getMatchNum(matches,ratio):
    '''返回特征点匹配数量和匹配掩码'''
    matchesMask = [[0, 0] for i in range(len(matches))]
    matchNum = 0
    for i,(m, n) in enumerate(matches):
        if m.distance < ratio*n.distance: #将距离比率小于ratio的匹配点删选出来
            matchesMask[i] = [1,0]
            matchNum += 1
    return (matchNum, matchesMask)



comparisonImageList = {} #记录比较结果
List = []
#创建SIFT特征提取器
sift = cv2.xfeatures2d.SIFT_create() 
#创建FLANN匹配对象
FLANN_INDEX_KDTREE = 0
indexParams = dict(algorithm = FLANN_INDEX_KDTREE, trees=5)
searchParams = dict(checks=50)
flann = cv2.FlannBasedMatcher(indexParams,searchParams)
num = 0
for pic in range(all_pic - 1):
    print(num)
    samplePath = path + str(num) + ".jpg"
    sampleImage = cv2.imread(samplePath,0)
    h, w = sampleImage.shape
    sampleImage = cv2.resize(sampleImage, (int(h/3),int(w/3)), interpolation = cv2.INTER_CUBIC)
    kp1, des1 = sift.detectAndCompute(sampleImage, None) #提取样本图片的特征

    queryPath = path + str(num + 1) + ".jpg" 
    queryImage = cv2.imread(queryPath, 0)
    h1, w1 = queryImage.shape
    queryImage = cv2.resize(queryImage, (int(h1/3), int(w1/3)), interpolation = cv2.INTER_CUBIC)
    kp2, des2 = sift.detectAndCompute(queryImage, None) #提取比对图片的特征
    matches = flann.knnMatch(des1, des2, k=2) #匹配特征点，为了删选匹配点，指定k为2，这样对样本图的每个特征点，返回两个匹配
    (matchNum, matchesMask) = getMatchNum(matches, 0.9) #通过比率条件，计算出匹配程度
    matchRatio = matchNum*100/len(matches)
    drawParams = dict(matchColor = (0,255,0),
                singlePointColor = (255,0,0),
                matchesMask = matchesMask,
                flags = 0)

    comparisonImageList[num] = matchRatio
    num += 1

ImageList = sorted(comparisonImageList,key=comparisonImageList.__getitem__,reverse=True)
for i in range(int(len(ImageList)/2)):
    if ImageList[i] == 0:
        List.append(1)
        continue
    if ImageList[i] == all_pic - 2:
        List.append(all_pic - 2)
        continue
    a, b = comparisonImageList.get(ImageList[i] - 1), comparisonImageList.get(ImageList[i] + 1)
    if a > b:
        List.append(ImageList[i])
    else:
        List.append(ImageList[i] + 1)
        
        
        
    

it = []
List.sort()
it = itertools.groupby(List)
for i,j in enumerate(it):
    os.remove(path + str(j[0]) + ".jpg")