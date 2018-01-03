import RPi.GPIO as GPIO
import time
import signal
import atexit



atexit.register(GPIO.cleanup)
servo1pin = 21
servo2pin = 20
GPIO.setmode(GPIO.BCM)
GPIO.setup(servo1pin, GPIO.OUT, initial=False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(servo2pin, GPIO.OUT, initial=False)

p1 = GPIO.PWM(servo1pin, 50)
p2 = GPIO.PWM(servo2pin, 50)

def servo1angle(angle):
    dutycircle = float(angle) / 18 + 2.5
    p1.ChangeDutyCycle(dutycircle)


def servo2angle(angle):
    dutycircle = float(angle) / 18 + 2.5
    p2.ChangeDutyCycle(dutycircle)


def servoinit():
    p1.start(0)
    p2.start(0)

def preparetouch():
    servo2angle(20)
    time.sleep(0.5)

def armleave():
     servo2angle(45)
     time.sleep(0.5)

def touch(touchtime):
    defaulttime = 0.5
    servo1angle(135)
    time.sleep(touchtime+defaulttime)
    servo1angle(90)

def touchtest(touchtime):
    preparetouch()
    touch(touchtime)
    time.sleep(0.5)
    armleave()

servoinit()
while(True):
    str = raw_input("Enter angle: ")
    touchtime = float(str)
    touchtest(touchtime)
