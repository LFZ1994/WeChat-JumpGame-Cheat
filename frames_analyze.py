import cv2
from getscreen import getScreen
import servo
from datetime import date
import getscreen
import os
import time
import datetime


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
    img = getScreen(filename)
    img_copy = img.copy()
    feature = cv2.imread('test pic/feature1.png')
    h,w,_ = feature.shape
    print w,h

    #re-size image to fit feature
    imgshape = img_copy.shape
    factor = imgshape[0]/640.0
    img = cv2.resize(img_copy,(int(imgshape[1]/factor),int(imgshape[0]/factor)),interpolation=cv2.INTER_CUBIC)
    img_copy = img.copy()
    rows,cols,_ = img.shape
    print rows,cols

    #find feature in frame
    res = cv2.matchTemplate(img,feature,cv2.TM_CCOEFF)
    # if res == None:
    #     return False
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    top_left = max_loc
    bottom_right = (top_left[0] + w, top_left[1] + h)
    print top_left,bottom_right

    #binary frame
    img_gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    bg_grayval1 = img_gray[20, 20]
    bg_grayval2 = img_gray[rows - 20, cols - 20]
    if bg_grayval1 > bg_grayval2:
        temp = bg_grayval1
        bg_grayval1 = bg_grayval2
        bg_grayval2 = temp
    print 'bg_grayval1',bg_grayval1,bg_grayval2
    img_canny = cv2.Canny(img_gray,15,bg_grayval1-15)
    for i in range(0,rows):
        for j in range(0,cols):
            if((i<int(cols*0.3))|(i>bottom_right[1])):
                img_canny[i,j] = 0
    # cv2.imshow('img_canny',img_canny)


    img_canny = cv2.bitwise_not(img_canny)

    #mark target point
    point1 = findTopPoint(img_canny,cols,rows)
    print 'point1=',point1
    cv2.circle(img,(point1[0],point1[1]),5,(255,0,0),2)
    if(point1[0]>(bottom_right[0]-13)):
        point2 = findRightPoint(img_canny,cols,rows)
    else:
        point2 = findLeftPoint(img_canny, cols, rows)
    print 'point1=',point2
    cv2.circle(img,(point2[0],point2[1]),5,(255,0,0),2)
    cv2.circle(img,(point1[0],point2[1]),5,(255,0,0),2)

    cv2.circle(img,(bottom_right[0]-13,bottom_right[1]),5,(255,0,0),2)
    cv2.line(img,(bottom_right[0]-13,bottom_right[1]),\
             (point1[0],point2[1]),(0,0,255),2)

    cv2.rectangle(img,top_left, bottom_right, 255, 2)

    savepath = '%s'%(path)+'/result/'+'%d'%(runtime)+'.jpg'
    print savepath
    cv2.imwrite(savepath,img)
    savepath = '%s' % (path) + '/canny/' + '%d' % (runtime) + '.jpg'
    print savepath
    cv2.imwrite(savepath,img_canny)
    savepath = '%s' % (path) + '/gray/' + '%d' % (runtime) + '.jpg'
    print savepath
    cv2.imwrite(savepath,img_gray)

    # cv2.imwrite('test pic/binary_r.jpg',img_canny)
    cv2.destroyAllWindows()

#get frame
cap = cv2.VideoCapture(0)
servo.servoinit()
runstep = 0
timestr = time.strftime('%Y-%m-%d-%H%M%S',time.localtime(time.time()))
path = "runlog/"+"%s"% (timestr)
os.mkdir(path)
os.mkdir('%s'%(path)+'/gray')
os.mkdir('%s'%(path)+'/canny')
os.mkdir('%s'%(path)+'/orign')
os.mkdir('%s'%(path)+'/result')
while(1):
    # timestart = time.time()
    ret,frame = cap.read()
    frame = cv2.transpose(frame)
    frame = cv2.flip(frame,1)
    cv2.imshow("frame",frame)
    cv2.imwrite('%s'%(path)+'/orign'+'/%d'%(runstep)+'.jpg', frame)
    servo.preparetouch()
    # result = analyseFrame('%s'%(path)+'/orign'+'/%d'%(runstep)+'.jpg',runstep,path)
    # # if result:
    # runstep += 1
    # # time.sleep(1)
    # timeend = time.time()
    # print timeend-timestart,'\r\n'
    if cv2.waitKey(1) & 0XFF == ord('q'):
        break
    # servo.preparetouch()
    # time.sleep(1)
    # servo.touch(0.5)
    # time.sleep(0.5)
    # servo.armleave()
    # time.sleep(1)

cap.release()
cv2.destroyAllWindows()

# # #test
# for i in range(23,25):
#     # analyseFrame('test pic/21.jpg')
#     # filename = 'test pic/'+'%d'+'.jpg'(i)
#     # filename = "test pic/%d.jpg"%(i)
#     filename = "test pic/"+"%d"% (i)+".jpg"
#     print filename,i
#     analyseFrame(filename,i)


cv2.waitKey(10000000)
cv2.destroyAllWindows()