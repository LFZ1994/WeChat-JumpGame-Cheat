import cv2
from getscreen import getScreen
import numpy as np
import math

def findTopPoint(img_binary,cols,rows):
    for i in range(int(rows*0.3),int(rows*0.9)):
        for j in range(int(cols*0.02),int(cols*0.98)):
            if(img_binary[i,j] == 0):
                point = [j,i]
                return point

def findRightPoint(img_binary,cols,rows):
    for i in range(int(cols*0.98),int(cols*0.02),-1):
        for j in range(int(rows*0.3),int(rows*0.9)):
            if(img_binary[j,i] == 0):
                point = [i,j]
                return point

def findLeftPoint(img_binary,cols,rows):
    for i in range(int(cols*0.02),int(cols*0.98)):
        for j in range(int(rows*0.3),int(rows*0.9)):
            if(img_binary[j,i] == 0):
                point = [i,j]
                return point

def analyseFrame(filename,runtime,path):
    # img = cv2.imread(filename)
    img = cv2.imread(filename)
    img = getScreen(img)
    # print type(img)
    if  type(img) is type(None) :
        return None
    else:
        img_copy = img.copy()
        feature = cv2.imread('test pic/feature.png')
        h,w,_ = feature.shape
        # print w,h

        #re-size image to fit feature
        imgshape = img_copy.shape
        factor = imgshape[0]/640.0
        img = cv2.resize(img_copy,(int(imgshape[1]/factor),int(imgshape[0]/factor)),interpolation=cv2.INTER_CUBIC)
        rows,cols,_ = img.shape
        img_hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)

        #find feature in frame
        res = cv2.matchTemplate(img,feature,cv2.TM_CCOEFF_NORMED)
        if type(res) == type(None):
            return None
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        top_left = max_loc
        bottom_right = (top_left[0] + w, top_left[1] + h)


        # clahe = cv2.createCLAHE(clipLimit=1.0, tileGridSize=(8, 8))
        # img = clahe.apply(img)
        # cv2.imshow('img_gray2', img);

        #find target land zone
        #get color mask
        '''this is used to solve yellow-gree target
        area can not find in white background when use Canny'''
        img_roi = img[int(cols * 0.4):bottom_right[1], 0:cols]

        # res = cv2.matchTemplate(img_roi,feature,cv2.TM_CCORR)
        # if type(res) == type(None):
        #     return None
        # else :
        #     print 'res ',res


        img_roi_hsv = cv2.cvtColor(img_roi,cv2.COLOR_BGR2HSV)
        # cv2.imshow("hsv", img_roi_hsv)

        lower_yellow = np.array([20, 50, 50])
        upper_yellow = np.array([42, 255, 255])
        mask_y = cv2.inRange(img_roi_hsv, lower_yellow, upper_yellow)
        kernel = np.ones((5, 5), np.uint8)
        mask_y = cv2.dilate(mask_y, kernel, iterations=1)
        mask_ycany = cv2.Canny(mask_y, 0, 100)
        mask_yNonZero = cv2.countNonZero(mask_ycany)

        # lower_white = np.array([0, 10, 90])
        # upper_white = np.array([60,20, 120])
        # mask_w = cv2.inRange(img_roi_hsv, lower_white, upper_white)
        # # kernel = np.ones((5, 5), np.uint8)
        # # mask_w = cv2.dilate(mask_w, kernel, iterations=1)
        # mask_wcany = cv2.Canny(mask_w, 0, 100)
        # mask_wNonZero = cv2.countNonZero(mask_wcany)



        img_roi_gray = cv2.cvtColor(img_roi,cv2.COLOR_BGR2GRAY)
        img_gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        # img_roi_gray = cv2.GaussianBlur(img_roi_gray, (5, 5), 0)

        # cv2.imshow('img_gray1',img_roi_gray);
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(4, 4))
        img_roi_gray = clahe.apply(img_roi_gray)

        # cv2.imshow('img_gray2',img_roi_gray);

        img_roi_canny = cv2.Canny(img_roi_gray,img_roi_gray[5,5]-50, img_roi_gray[5,5]-5)
        if (mask_yNonZero < 500)&(mask_yNonZero > 20):
            print 'mask_yNonZero',mask_yNonZero
            # cv2.imshow('mask',mask_y)
            # cv2.imshow('mask_ycany', mask_ycany)
            mask_ycany = cv2.Canny(mask_y,0, 100)
            img_roi_canny = cv2.bitwise_or(img_roi_canny,mask_ycany)

        # if mask_wNonZero < 1000:
        #     cv2.imshow('mask',mask_w)
        #     cv2.imshow('mask_wcany', mask_wcany)
        #     mask_wcany = cv2.Canny(mask_y,0, 100)
        #     img_roi_canny = cv2.bitwise_or(img_roi_canny,mask_wcany)
        #

        kernel = np.ones((3, 3), np.uint8)
        img_roi_canny = cv2.dilate(img_roi_canny, kernel, iterations=1)

        # img_roi = img_canny[int(cols*0.4):bottom_right[1],0:cols]

        img_roi_canny = cv2.bitwise_not(img_roi_canny)

        savepath = '%s' % (path) + '/gray/' + '%d' % (runtime) + '.jpg'
        # print savepath
        cv2.imwrite(savepath,img_gray)

        savepath = '%s' % (path) + '/canny/' + '%d' % (runtime) + '.jpg'
        # print savepath
        cv2.imwrite(savepath,img_roi_canny)

        #mark target point
        rows_r, cols_r,_ = img_roi.shape
        point1 = findTopPoint(img_roi_canny,cols_r,rows_r)
        # print 'point1=',point1
        if(point1[0]>(bottom_right[0]-13)):
            point2 = findRightPoint(img_roi_canny,cols_r,rows_r)
        else:
            point2 = findLeftPoint(img_roi_canny, cols_r, rows_r)
        # print 'point2=',point2

        point1[1] = point1[1] + int(cols * 0.4)
        point2[1] += int(cols * 0.4)
        print 'point1=',point1,'point2=',point2


        cv2.circle(img,(point1[0],point1[1]),5,(255,0,0),2)
        if point2[0]<point1[0]:
            point2[0] += 20
            point2[1] -= 20
        cv2.circle(img,(point2[0],point2[1]),5,(255,0,0),2)
        cv2.circle(img,(point1[0],point2[1]),5,(255,0,0),2)


        # print 'HSV=',img_hsv[point1[0],point2[1]]

        cv2.circle(img,(bottom_right[0]-13,bottom_right[1]),5,(255,0,0),2)
        cv2.line(img,(bottom_right[0]-13,bottom_right[1]),\
                 (point1[0],point2[1]),(0,0,255),2)

        cv2.rectangle(img,top_left, bottom_right, 255, 2)

        # hsv_gray = cv2.cvtColor(img_roi_hsv,cv2.COLOR_BGR2GRAY);

        # cv2.imshow('img',img)
        # cv2.imshow('img_canny',img_roi_canny)

        distance1 = math.hypot(rows,cols)
        distance2 = math.hypot((point1[0]-bottom_right[0]+13),(point2[1]-bottom_right[1]))
        distance = float(14*distance2/distance1)
        touchtime = (distance-0.3)/5.5
        txtName = '%s' % (path) + '/runlog.txt'
        f = open(txtName, 'a')
        newcontex = 'result'+'\t'+'%d'%(runtime)+'\t'+'%f'%(distance1)+'\t'+\
                    '%03f'%(distance2)+'\t'+'%03f'%(distance)+'\t'+\
                    '%03f'%(touchtime)+'\n'
        f.write(newcontex)
        f.close()
        print newcontex
        savepath = '%s'%(path)+'/result/'+'%d'%(runtime)+'.jpg'
        # print savepath
        cv2.imwrite(savepath,img)

        # cv2.imshow('result',img)
        # cv2.waitKey(100000);
        # cv2.imwrite('test pic/binary_r.jpg',img_canny)
        # cv2.destroyAllWindows()
        return touchtime

# while True:
#     analyseFrame('0.jpg',1,)
#     if cv2.waitKey(1) & 0XFF == ord('q'):
#         break
# cv2.destroyAllWindows()