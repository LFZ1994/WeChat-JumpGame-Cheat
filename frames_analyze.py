import cv2
import numpy as np

img = cv2.imread('test pic/3.jpg')
img_copy = img.copy()
feature = cv2.imread('test pic/feature1.png')
h,w,_ = feature.shape

#cv2.imshow('img',img)
#cv2.imshow('feature',feature)
print w,h
#re-size image to fit feature
imgshape = img_copy.shape
factor = imgshape[0]/640
img = cv2.resize(img_copy,(imgshape[1]/factor,imgshape[0]/factor),interpolation=cv2.INTER_CUBIC)
img_copy = img.copy()
#find feature in frame
res = cv2.matchTemplate(img,feature,cv2.TM_CCOEFF)
min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
top_left = max_loc
bottom_right = (top_left[0] + w, top_left[1] + h)


#find land box in frame
img_gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
ret,thresh = cv2.threshold(img_gray,127,255,0)
image, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
img = cv2.drawContours(img, contours, 3, (0,255,0), 3)
img_canny = cv2.Canny(img_gray,100,150,apertureSize = 5)
circles = cv2.HoughCircles(img_canny,cv2.HOUGH_GRADIENT,1,20,
param1=50,param2=30,minRadius=60,maxRadius=100)
print circles
circles = np.uint16(np.around(circles))
for i in circles[0,:]:
    # draw the outer circle
    cv2.circle(img,(i[0],i[1]),i[2],(0,255,0),2)
    # draw the center of the circle
    cv2.circle(img,(i[0],i[1]),2,(0,0,255),3)

img = cv2.drawContours(img, contours, 3, (0,255,0), 3)
cv2.imshow('canny',img_canny)
cv2.imshow('img_gray',img_gray)
cv2.rectangle(img,top_left, bottom_right, 255, 2)
cv2.imshow('result',img)

#cv2.imwrite('test pic/canny.jpg',img_canny)


cv2.waitKey(10000000)
cv2.destroyAllWindows()