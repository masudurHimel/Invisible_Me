import cv2
import numpy as np
import time
import argparse

temp_parser = argparse.ArgumentParser()
temp_parser.add_argument("--video")
args = temp_parser.parse_args()
print("Hey There !! Prepare to get invisible.....")

# Creating an VideoCapture object
videoCap = cv2.VideoCapture(args.video if args.video else 0)

time.sleep(3)
acountCapture = 0
background=0

# Capturing and storing the static background frame
for i in range(60):
	ret,background = videoCap.read()

while(videoCap.isOpened()):
	ret, img = videoCap.read()
	if not ret:
		break
	acountCapture+=1
	# Converting the color space from BGR to HSV
	hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
	
	# Generating mask to detect red color
	#here I have used red color as my invisible cloak
	#in order to change into another color, just replace these values with your corresponding color's HSV value
	lower_red_threshold = np.array([0,120,70])
	upper_red_threshold = np.array([10,255,255])
	mask1 = cv2.inRange(hsv,lower_red_threshold,upper_red_threshold)

	lower_red_threshold = np.array([170,120,70])
	upper_red_threshold = np.array([180,255,255])
	mask2 = cv2.inRange(hsv,lower_red_threshold,upper_red_threshold)

	mask1 = mask1+mask2

	# Mask to determine the red color
	mask1 = cv2.morphologyEx(mask1, cv2.MORPH_OPEN, np.ones((3,3),np.uint8),iterations=2)
	mask1 = cv2.dilate(mask1,np.ones((3,3),np.uint8),iterations = 1)
	mask2 = cv2.bitwise_not(mask1)

	# final output
	res1 = cv2.bitwise_and(background,background,mask=mask1)
	res2 = cv2.bitwise_and(img,img,mask=mask2)
	final = cv2.addWeighted(res1,1,res2,1,0)

	cv2.imshow('Magic !!!',final)
	key = cv2.waitKey(10)
	if key == 27:
		break