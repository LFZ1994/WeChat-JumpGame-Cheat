import cv2
import time
def findLeftTopPoint(img_binary,rows,cols):
    minsum = 0xffff
    for i in range(0,int(cols*0.2)):
        for j in range(0,int(rows*0.2)):
            if(img_binary[j,i] == 255):
                if(i+j<minsum):
                    minsum = (i+j)
                    point = [i,j]
    return point

def findRightBottomPoint(img_binary,rows,cols):
    maxsum = 0
    for i in range(cols-1,int(cols*0.7),-1):
        for j in range(rows-1,int(rows*0.7),-1):
            if(img_binary[j,i] == 255):
                if(i+j>maxsum):
                    maxsum = (i+j)
                    point = [i,j]
    return point

def getScreen(filename):
    start = time.time()
    img = cv2.imread(filename)
    img_canny = cv2.Canny(img,127,255)
    cv2.imshow('img',img)
    cv2.imshow('img_canny',img_canny)
    rows, cols, _ = img.shape
    point1 = findLeftTopPoint(img_canny,rows, cols)
    point2 = findRightBottomPoint(img_canny,rows,cols)
    print point1,point2
    img_roi = img[point1[1]+2:point2[1]-2,point1[0]+2:point2[0]-2]
    return img_roi

# getScreen('runlog/2018-01-01-173007/orign/0.jpg')
# cv2.waitKey(10000000)
# cv2.destroyAllWindows()





