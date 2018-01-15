import cv2
from getscreen import getScreen

cap = cv2.VideoCapture(0)

while True:

    ret, frame = cap.read()
    # frame = cv2.VideoCapture.get(cap)
    frame = cv2.transpose(frame)
    frame = cv2.flip(frame, 1)
    frame = getScreen(frame)
    if frame != None:
        cv2.imshow('orignal',frame)
    # cv2.imshow('orignal', frame)
    if cv2.waitKey(1) & 0XFF == ord('q'):
        break
cv2.destroyAllWindows()
cap.release()
cv2.destroyAllWindows()