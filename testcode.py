import cv2
from frames_analyze import analyseFrame
import os
import numpy as np
import time

timestr = time.strftime('%Y-%m-%d-%H%M%S', time.localtime(time.time()))
path = "runlog/" + "%s" % (timestr)
os.mkdir(path)
os.mkdir('%s' % (path) + '/gray')
os.mkdir('%s' % (path) + '/canny')
os.mkdir('%s' % (path) + '/orign')
os.mkdir('%s' % (path) + '/result')
for i in range(0,33):
    filname = 'runlog/2018-01-15-005836/orign/'+'%d'%(i)+'.jpg'
    analyseFrame(filname,i,path)
    #
    # img = cv2.imread(filname)
    # screen = getScreen(img)
    # img_gray = cv2.cvtColor(screen,cv2.COLOR_BGR2GRAY)
    # blur = cv2.GaussianBlur(img_gray, (3,3), 0)
    # ret1,th1 = cv2.threshold(blur, 0, 255,\
    #                           cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    # th2 = cv2.adaptiveThreshold(img_gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
    #                            cv2.THRESH_BINARY, 11, 2)
    # th3 = cv2.adaptiveThreshold(img_gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C,\
    #                             cv2.THRESH_BINARY, 11, 2)
    # img_temp = np.hstack((img_gray,th1,th2,th3))
    # cv2.imshow('img_gray', img_temp)
    #
    # equ = cv2.equalizeHist(img_gray)
    # txtName = '1111.txt'
    # f = open(txtName, 'a')
    # distance = 1.00
    # touchtime = 1.001
    # newcontex = 'result'+'%f'%(distance)+'\n'
    # f.write(newcontex)
    # f.close()
    #
    #
    # # clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    # # cl1 = clahe.apply(img_gray)
    # img_hsv = cv2.cvtColor(screen,cv2.COLOR_BGR2HSV)
    # img_canny = cv2.Canny(img_gray,15,90)
    # # img_canny = cv2.blur(img_canny, (3, 3))
    # kernel = np.ones((3, 3), np.uint8)
    # img_canny = cv2.dilate(img_canny, kernel, iterations=1)
    # _, img_canny = cv2.threshold(img_canny, 100, 255, cv2.THRESH_BINARY)
    # _,contours,hierarchy = cv2.findContours\
    #     (img_canny, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # cnt = contours[0]
    # #
    # # for i in range(0,32):
    # #     cnt = contours[i]
    # #     x, y, w, h = cv2.boundingRect(cnt)
    # #     rect = cv2.minAreaRect(cnt)
    # #     print rect
    # #     box = boxPoints(rect)
    # #     box = np.int0(box)
    # #     screen = cv2.rectangle(screen, (x, y), (x + w, y + h), (0, 255, 0), 2)
    # #     screen = cv2.drawContours(screen, [box], 0, (0, 0, 255), 2)
    #
    # cv2.imshow('screen',screen)
    # cv2.imshow('img_canny', img_canny)
    # cv2.imshow('img_hsv', img_hsv)
    print filname
    while True:
        if cv2.waitKey(1) & 0XFF == ord('q'):
            break
cv2.destroyAllWindows()