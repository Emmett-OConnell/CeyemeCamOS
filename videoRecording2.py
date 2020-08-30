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
if i==0:
        GPIO.output(3, 0)
        print ('no motion')
while i==0:
        i=GPIO.input(7) 
i=GPIO.input(7)
if i==1:
        camera.start_recording('/home/pi/video.h264')
        print('Recording')
        GPIO.output(3, 1)
while i==1:
        i=GPIO.input(7)
if i==0:
        GPIO.output(3, 0)
        camera.stop_recording()
        now = datetime.now()
        dt_string = now.strftime("%d_%m_%Y_%H_%M_%S")
        vid = dt_string+cam
        os.system('ffmpeg -i video.h264 -vf vflip -c:a copy video1.h264')
        os.system('rm video.h264')
        os.system('ffmpeg -i video1.h264 -vf hflip -c:a copy video.h264')
        os.system('rm video1.h264')
        os.system('ffmpeg -i video.h264 -vcodec copy '+vid+'.mp4')
        os.system('rm video.h264')
        os.system('scp cam1vid'+vid+'.mp4 pi@Ceyemore.local:/home/pi/Videos/Newvids')
        os.system('mv '+vid+'.mp4 v_storage2')
        os.system('ssh pi@Cam3.local python videoRecording3.py')

