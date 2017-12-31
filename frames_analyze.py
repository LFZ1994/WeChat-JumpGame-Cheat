import cv2
import numpy as np
from matplotlib import pyplot as plt
#find profile
def findTopPoint(img_binary,cols,rows):
    for i in range(200,580):
        for j in range(0,cols):
            if(img_binary[i,j] == 0):
                point = [j,i]
                return point

def findRightPoint(img_binary,cols,rows):
    for i in range(cols-1,0,-1):
        for j in range(200,580):
            if(img_binary[j,i] == 0):
                point = [i,j]
                return point




img = cv2.imread('test pic/4.jpg')
img_copy = img.copy()
feature = cv2.imread('test pic/feature1.png')
h,w,_ = feature.shape
print w,h

bg_rgb = img[0,0]

#re-size image to fit feature
imgshape = img_copy.shape
factor = imgshape[0]/640
img = cv2.resize(img_copy,(imgshape[1]/factor,imgshape[0]/factor),interpolation=cv2.INTER_CUBIC)
img_copy = img.copy()
rows,cols,_ = img.shape
print rows,cols

#find feature in frame
res = cv2.matchTemplate(img,feature,cv2.TM_CCOEFF)
min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
top_left = max_loc
bottom_right = (top_left[0] + w, top_left[1] + h)
print top_left,bottom_right

#binary frame
img_gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
bg_grayval1 = img_gray[0,0]
bg_grayval2 = img_gray[rows-1,cols-1]
if bg_grayval1>bg_grayval2:
    temp = bg_grayval1
    bg_grayval1 = bg_grayval2
    bg_grayval2 = temp
img_binary = img_gray.copy()
print img_gray[0,0],img_gray[rows-1,cols-1]
for i in range(0,rows):
    for j in range(0,cols):
        if((i<200)|(i>580)):
            img_binary[i,j] = 255
        else:
            if (img_gray[i,j] >= bg_grayval1-1)&(img_gray[i,j] <= bg_grayval2+1):
                img_binary[i, j] = 255
            else:
                img_binary[i,j] = 0
                # print img_gray[i,j], bg_gray,i,j
cv2.imshow('img_binary',img_binary)

#filter noise
kernel = np.ones((3,3),np.uint8)
erode=cv2.erode(img_binary,None,iterations=1)
img_binary = cv2.dilate(erode,None,iterations=1)
cv2.imshow('img_binaryH',img_binary)
cv2.medianBlur(img_binary,3)

#find target box in frame
point1 = findTopPoint(img_binary,cols,rows)
print 'point1=',point1
cv2.circle(img,(point1[0],point1[1]),5,(255,0,0),3)
point2 = findRightPoint(img_binary,cols,rows)
print 'point1=',point2
cv2.circle(img,(point2[0],point2[1]),5,(255,0,0),3)
cv2.circle(img,(point1[0],point2[1]),5,(255,0,0),3)

img_canny = cv2.Canny(img_gray,127,244)
cv2.imshow('img_canny',img_canny)
# img_binary = cv2.bitwise_not(img_binary)
# cv2.imshow('img_binaryH',img_binary)
# _,contours,hierarchy = cv2.findContours(img_binary,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
# print contours
# if contours != None:
#     img_binary = cv2.drawContours(img, contours, 3, (0,255,0), 3)



# mask = np.zeros(img.shape[:2],np.uint8)
# bgdModel = np.zeros((1,65),np.float64)
# fgdModel = np.zeros((1,65),np.float64)
# rect = (0,0,w-1,h-1)
# cv2.grabCut(img_copy,mask,rect,bgdModel,fgdModel,5,cv2.GC_INIT_WITH_RECT)

# mask2 = np.where((mask==2)|(mask==0),0,1).astype('uint8')
# img = img_copy*(mask2[:,:,np.newaxis])

# cv2.imshow('mask2',img_mask)

#find land box in frame

#img = cv2.drawContours(img, contours, 3, (0,255,0), 3)



# img_canny = cv2.Canny(img_gray,100,150,apertureSize = 5)
# circles = cv2.HoughCircles(img_canny,cv2.HOUGH_GRADIENT,1,20,
# param1=50,param2=30,minRadius=60,maxRadius=100)
#
# if circles!=None:
#     print circles
#     circles = np.uint16(np.around(circles))
#     for i in circles[0,:]:
#         # draw the outer circle
#         cv2.circle(img,(i[0],i[1]),i[2],(0,255,0),2)
#         # draw the center of the circle
#         cv2.circle(img,(i[0],i[1]),2,(0,0,255),3)
# else:
#     print 'No circle'

# cv2.imshow('canny',img_canny)
# cv2.imshow('img_gray',img_gray)
cv2.rectangle(img,top_left, bottom_right, 255, 2)
#  cv2.imshow('result',img)

# cv2.imwrite('test pic/gray.jpg',img_gray)
# cv2.imwrite('test pic/binary_r.jpg',img_binary)

print img[0,0]
#print img[w,h]
# plt.subplot(231),plt.imshow(img)
# plt.title('orignal'),plt.xticks([]),plt.yticks([])
# plt.subplot(232),plt.imshow(img_gray,cmap='gray')
# plt.title('gray'),plt.xticks([]),plt.yticks([])
# plt.subplot(233),plt.imshow(thresh,cmap='gray')
# plt.title('thresh'),plt.xticks([]),plt.yticks([])
# # plt.subplot(234),plt.imshow(img_canny,cmap='gray')
# # plt.title('img_canny'),plt.xticks([]),plt.yticks([])
# plt.subplot(234),plt.imshow(imgAdapt ,cmap='gray')
# plt.title('imgAdapt'),plt.xticks([]),plt.yticks([])
# plt.subplot(235),plt.imshow(imgOtsu ,cmap='gray')
# plt.title('imgOtsu'),plt.xticks([]),plt.yticks([])
# plt.subplot(236),plt.imshow(img_mask ,cmap='gray')
# plt.title('img_mask'),plt.xticks([]),plt.yticks([])
# plt.show()

cv2.imshow('gray',img_gray)

cv2.imshow('img',img)

cv2.waitKey(10000000)
cv2.destroyAllWindows()