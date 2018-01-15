from frames_analyze import analyseFrame
import getscreen
import servo
import cv2
import os
import time

# get frame
servo.servoinit()
servo.armleave()
runstep = 0
timestr = time.strftime('%Y-%m-%d-%H%M%S', time.localtime(time.time()))
path = "runlog/" + "%s" % (timestr)
os.mkdir(path)
os.mkdir('%s' % (path) + '/gray')
os.mkdir('%s' % (path) + '/canny')
os.mkdir('%s' % (path) + '/orign')
os.mkdir('%s' % (path) + '/result')
# time.sleep(2)
# cap = cv2.VideoCapture(0)
# ret, frame = cap.read()
# cv2.imwrite('%s' % (path) + '/orign' + '/%d' % (runstep) + '.jpg', frame)
# result = analyseFrame('%s' % (path) + '/orign' + '/%d' % (runstep) + '.jpg', runstep, path)
# cap.release()
runflag = True

while (1):

    # cv2.imshow('frame',frame)
    if runflag:
        runflag = False
        timestart = time.time()
        cap = cv2.VideoCapture(0)
        time.sleep(0.5)
        ret, frame = cap.read()
        frame = cv2.transpose(frame)
        frame = cv2.flip(frame, 1)
        cap.release()

        cv2.imwrite('%s' % (path) + '/orign' + '/%d' % (runstep) + '.jpg', frame)
        servo.preparetouch()
        result = analyseFrame('%s' % (path) + '/orign' + '/%d' % (runstep) + '.jpg', runstep, path)
        print '%s' % (path) + '/orign' + '/%d' % (runstep) + '.jpg', runstep, path
        if result == None:
            runflag = servo.armleave()
            time.sleep(1)
            continue
        # cv2.destroyAllWindows()
        servo.touch(result)
        # if result:
        runstep += 1
        # time.sleep(1)
        timeend = time.time()

        print timeend - timestart, '\r\n'
        # time.sleep(2)
        runflag = servo.armleave()
        # time.sleep(0.5)
    if cv2.waitKey(1) & 0XFF == ord('q'):
        break

cv2.destroyAllWindows()