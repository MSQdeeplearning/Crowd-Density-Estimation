# -*- coding: utf-8 -*-
"""
Created on Fri May 24 23:30:54 2019

@author: msq
"""

import cv2
vc = cv2.VideoCapture("C://Users//Acer//Desktop//3//waitan.mp4")
c = 1
num = 0
if vc.isOpened():    
    rval,frame = vc.read()
else:    
    rval = False
while rval:    
    rval,frame=vc.read() 
    if c % 10 == 0:   
        cv2.imwrite('C://Users//Acer//Desktop//waitan//'+str(num)+'.jpg',frame)
        num += 1
        cv2.waitKey(1)
    c = c+1  
    print(c)
vc.release()
cv2.destroyAllWindows()