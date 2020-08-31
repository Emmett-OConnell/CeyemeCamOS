import RPi.GPIO as GPIO
import time
import os
import sys
import socket
from datetime import datetime
from picamera import PiCamera
camera = PiCamera()
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(7, GPIO.IN)         #Read output from PIR motion sensor
GPIO.setup(3, GPIO.OUT)         #LED output pin
i=GPIO.input(7)
cam = socket.gethostname()
while i==0:
	i=GPIO.input(7) 
	GPIO.output(3, 0)
	print ('no motion')
i=GPIO.input(7)
if i==1:
	camera.start_recording('/home/pi/video.h264')
while i==1:
	print('Recording')
	i=GPIO.input(7)
	GPIO.output(3, 1)
if i==0:
	camera.stop_recording()
	now = datetime.now()
	dt_string = now.strftime("%Y_%m_%d_%H_%M_%S")
	vid = dt_string+cam
	os.system('ffmpeg -i video.h264 -vf vflip -c:a copy video1.h264')
        os.system('rm video.h264')
        os.system('ffmpeg -i video1.h264 -vf hflip -c:a copy video.h264')
	os.system('rm video1.h264')
	os.system('ffmpeg -i video.h264 -vcodec copy '+vid+'.mp4')
	os.system('rm video.h264')
	os.system('scp '+vid+'.mp4 pi@Ceyemore.local:/home/pi/Videos/Newvids')
	os.system('mv '+vid+'.mp4 v_storage')
