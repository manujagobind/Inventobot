#!/usr/bin/env python

import cv2
import numpy as np
import os
import rospy
from std_msgs.msg import String

rospy.init_node('cam', anonymous=True)
pub = rospy.Publisher('dir', String, queue_size=10)
rate = rospy.Rate(10)

kernel=np.ones((9,9),np.uint8)
disc = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
switch = False		#True for depth adjustment

def helper():
	ret={}
	os.chdir(os.getcwd() + '/static')
	files=[string for string in os.listdir(os.getcwd()) if string.endswith('.png')]
	for item in files:
		roi = cv2.imread(item)
		hsv = cv2.cvtColor(roi,cv2.COLOR_BGR2HSV)
		roihist = cv2.calcHist([hsv],[0, 1], None, [180, 256], [0, 180, 0, 256] )
		cv2.normalize(roihist,roihist,0,255,cv2.NORM_MINMAX)
		name=item.split('.')[0]
		ret[name] = roihist
	return ret

def backproject(roihists,images,i,hsvt):
	dst = cv2.calcBackProject([hsvt],[0,1],roihists[images+str(i)],[0,180,0,256],1)
	cv2.filter2D(dst,-1,disc,dst)
	ret,thresh = cv2.threshold(dst,50,255,0)
	thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
	return thresh

def multipleBackProjections(roihists,images,lt,hsvt,b,g,r):
	global target
	area = 0.0
	for i in range(lt):
		t0=backproject(roihists,images,i,hsvt)
		if (i!=0):
			t1 = cv2.bitwise_or(t1,t0)
		else:
			t1=t0
	#(_, cnts, _) = cv2.findContours(t1.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
	(cnts,_) = cv2.findContours(t1.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
	centroid = (0,0)
	if cnts:
		c = max(cnts, key=cv2.contourArea)
		rect = cv2.minAreaRect(c)
		#box = cv2.boxPoints(rect)
		box = cv2.cv.BoxPoints(rect)
		box = np.int0(box)
		cv2.drawContours(target,[box],0,(b,g,r),2)
		area = cv2.contourArea(c)
		(x,y),radius = cv2.minEnclosingCircle(c)
		centroid = (int(x),int(y))
		radius = 2
		img = cv2.circle(target,centroid,radius,(b,g,r),-1)

	return t1, centroid, area

def callback(data):

	global cap
	global target
	cap = cv2.VideoCapture(0)
	cv2.namedWindow('image',cv2.WINDOW_NORMAL)
	cv2.namedWindow('image1',cv2.WINDOW_NORMAL)
	screen_centre = (int(cap.get(3) / 2), int(cap.get(4) / 2))
	roi_leftCorner = (screen_centre[0] - 60, screen_centre[1] - 100)
	roi_rightCorner = (screen_centre[0] + 60, screen_centre[1] + 100)
	roihists=helper()
	L = [0 for i in range(25)]
	counter = 0

	if data.data == 'start':
		while(cap.isOpened()):

			_, frame = cap.read()
			roi1 = frame[roi_leftCorner[1]:roi_rightCorner[1], roi_leftCorner[0]:roi_rightCorner[0]]
			cv2.rectangle(frame, roi_leftCorner, roi_rightCorner, (120, 120, 120), 1)
			k = cv2.waitKey(1) & 0xFF
			if cv2.waitKey(1) & 0xFF == 27:
				cv2.imshow('image',frame)
			else:
				target=frame
				hsvt = cv2.cvtColor(target,cv2.COLOR_BGR2HSV)
				thresh_yel, centroid_yel, contourArea_yel = multipleBackProjections(roihists,'yel',8,hsvt,0,255,0)
				cv2.imshow('image',frame)

				L[counter] = contourArea_yel
				counter+=1

				angular_msg, depth_msg = 'X', 'X'
				if counter is 25:
					if centroid_yel[0] - screen_centre[0] >= 10:
						angular_msg = 'L'		#Left
						#print 'Attempting angular adjustment'
						#print "Prediction: Move Bot to the Left"
						angular_adjust = False
						switch = False
					elif screen_centre[0] - centroid_yel[0] >= 10:
						angular_msg = 'R'		#Right
						#print 'Attempting angular adjustment'
						#print "Prediction: Move Bot to the right"
						angular_adjust = False
						switch = False
					else:
						angular_msg = 'A'		#Angular
						#print "Prediction: Bot set at optimal angular distance"
						angular_adjust = True
						switch = True

					if switch:
						tracked_area = int(sum(L) / len(L))
						if tracked_area in range(4673, 5872):
							depth_msg = 'D'		#Depth
							#print "Prediction: Bot set at optimal linear distance"
							depth_adjust = True
						else:
							depth_adjust = False
							if tracked_area < 4673:
								depth_msg = 'F'		#Forward
								#print 'Attempting depth adjustment'
								#print "Prediction: Move the Bot forward"
							else:
								depth_msg = 'B'		#Backward
								#print 'Attempting depth adjustment'
								#print "Prediction: Move the Bot backward"

					if not angular_adjust:
						#msg = angular_msg
						pub.publish(angular_msg)
						rospy.sleep(21)
					elif not depth_adjust:
						pub.publish(depth_msg)
						rospy.sleep(3)
					elif angular_adjust and depth_adjust:
						#print 'Bot Adjustment Sucessful.'
						pub.publish('S')
					else:
						pass

					counter = 0
				cv2.imshow('image1',thresh_yel)

			k = cv2.waitKey(1) & 0xFF
			if k == 27:
				cap.release()
				break

def main:
	rospy.Subscriber('kbki', String, callback)
	rospy.spin()

if __name__ == '__main__':
	main()
