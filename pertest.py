import RPi.GPIO as GPIO
import time
import os
import sys
from datetime import datetime
from picamera import PiCamera
camera = PiCamera()
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.IN)         #Read output from PIR motion sensor
GPIO.setup(3, GPIO.OUT)         #LED output pin
i=GPIO.input(11)
while i==0:
	i=GPIO.input(11) 
	GPIO.output(3, 0)
	print ('no motion')
i=GPIO.input(11)
if i==1:
	camera.start_recording('/home/pi/video.h264')
while i==1:
	i=GPIO.input(11)
	GPIO.output(3, 1)
if i==0:
	camera.stop_recording()
	now = datetime.now()
	dt_string = now.strftime("%d_%m_%Y_%H_%M_%S")
	os.system('ffmpeg -i video.h264 -vcodec copy cam1vid'+dt_string+'.mp4')
	os.system('scp cam1vid'+dt_string+'.mp4 pi@Ceyemore.local:/home/pi/Videos/Newvids')

