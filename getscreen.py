import cv2
import numpy as np

def boxPoints(rect):
    angle = float(rect[2]*(3.14159)/180)
    box= [[0,0],[0,0],[0,0],[0,0]]
    a = float(np.cos(angle))*0.5
    b = float(np.sin(angle))*0.5
    box[0][0] = rect[0][0]-a*rect[1][0]-b*rect[1][1]
    box[0][1] = rect[0][1]-b*rect[1][0]+a*rect[1][1]
    box[1][0] = rect[0][0]-a*rect[1][0]+b*rect[1][1]
    box[1][1] = rect[0][1]-b*rect[1][0]-a*rect[1][1]
    box[2][0] = 2*rect[0][0] - box[0][0]
    box[2][1] = 2*rect[0][1] - box[0][1]
    box[3][0] = 2*rect[0][0] - box[1][0]
    box[3][1] = 2*rect[0][1] - box[1][1]
    return box

def getScreen(img):
    rows, cols, _ = img.shape
    img_roi = img[int(rows*0.02):int(rows*0.99), int(cols*0.02): int(cols*0.98)]
    img = img_roi
    rows, cols, _ = img.shape
    img_gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    img_canny = cv2.Canny(img_gray,40,180)
    # img_canny = cv2.blur(img_canny, (3, 3))
    kernel = np.ones((3, 3), np.uint8)
    img_canny = cv2.dilate(img_canny, kernel, iterations=1)
    # cv2.imshow('canny',img_canny)
    #find contoursA
    if cv2.__version__ < '3.0':
        contours,hierarchy = cv2.findContours\
        (img_canny, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    else:
        _,contours,hierarchy = cv2.findContours \
            (img_canny, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnt = contours[0]
    x, y, w, h = cv2.boundingRect(cnt)
    rect = cv2.minAreaRect(cnt)
    # print rect
    box = boxPoints(rect)
    box = np.int0(box)
    maxval = box[0][0] + box[0][1]
    maxpos = 0
    for i in range(0,4):
        if(box[i][0]+box[i][1]>maxval):
            maxval = box[i][0]+box[i][1]
            maxpos = i
    if maxpos != 0:
        temp = [box[maxpos][0],box[maxpos][1]]
        if(maxpos == 1):
            box[1] = box[2]
            box[2] = box[3]
            box[3] = box[0]
            box[0] = temp
        if(maxpos == 2):
            box[1] = box[3]
            box[2] = box[0]
            box[3] = box[1]
            box[0] = temp
        if(maxpos == 3):
            box[3] = box[2]
            box[2] = box[1]
            box[1] = box[0]
            box[0] = temp
    # print box
    pts1 = np.float32([box[2],box[1],box[0]])
    pts2 = np.float32( [box[2],[box[2][0],box[1][1]],[box[0][0],box[1][1]]])
    M = cv2.getAffineTransform(pts1, pts2)
    dst = cv2.warpAffine(img, M, (cols, rows))
    img_roi = dst[box[2][1]+7:box[1][1]-5,box[2][0]+7:box[0][0]-5]
    rows, cols, _ = img_roi.shape
    if rows < 500:
        # print box
        cv2.imwrite('runlog/canny.jpg', img_canny)
        cv2.imwrite('runlog/img.jpg', img)
        cv2.imwrite('runlog/img_roi.jpg', img_roi)
        return None
    # print 'rows',rows,'cols',cols,(float(cols)/rows)
    # cv2.imshow('img',img_roi)
    return img_roi

# for i in range(0,28):
#     filname = '%d'%(i)+'.jpg'
#     img = cv2.imread(filname)
#     screen = getScreen(img)
#     cv2.imshow('screen',screen)
#     while True:
#         if cv2.waitKey(1) & 0XFF == ord('q'):
#             break
# cv2.destroyAllWindows()