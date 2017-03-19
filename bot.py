#!/usr/bin/env python

import time
import math
import rospy
from datetime import datetime
from geometry_msgs.msg import Twist
from std_msgs.msg import String

rospy.init_node('bot', anonymous=True)
pub = rospy.Publisher('/mobile_base/commands/velocity', Twist, queue_size=1)
pub1 = rospy.Publisher('kbki', String, queue_size=10)
pub2 = rospy.Publisher('grab', String, queue_size=10)
rate = rospy.Rate(0.5)

def turn_left():
	t1 = datetime.now()
	t2 = datetime.now()
	delta = t2 - t1
	#print delta.total_seconds()
	while delta.total_seconds() <= 1.58 * 4.759988:
		#print delta.total_seconds()
		#rate.sleep()
		twist = Twist()
		twist.angular.z = 0.33
		pub.publish(twist)
		#rate.sleep()
		t2 = datetime.now()
		delta = t2 - t1

def turn_right():
	t1 = datetime.now()
	t2 = datetime.now()
	delta = t2 - t1
	#print delta.total_seconds()
	while delta.total_seconds() <= 1.58 * 4.759988:
		#print delta.total_seconds()
		#rate.sleep()
		twist = Twist()
		twist.angular.z = -0.33
		pub.publish(twist)
		#rate.sleep()
		t2 = datetime.now()
		delta = t2 - t1

def move_left():
	print 'Bot: Moving Left'
	turn_left()
	rospy.sleep(1)
	move_forward()
	rospy.sleep(1)
	turn_right()

def move_right():
	print 'Bot: Moving Right'
	turn_right()
	rospy.sleep(1)
	move_forward()
	rospy.sleep(1)
	turn_left()

def move_forward():
	print 'Bot: Moving Forward'
	twist = Twist()
	twist.linear.x = 0.05
	pub.publish(twist)


def	move_backward():
	print 'Bot: Moving Backward'
	twist = Twist()
	twist.linear.x = -0.05
	pub.publish(twist)

def callback(data):
	if data.data == 'L':
		move_right()
	elif data.data == 'R':
		move_left()
	elif data.data == 'F':
		move_forward()
	elif data.data == 'B':
		move_backward()
	elif data.data == 'S':
		print "Success"
		pub2.publish('Grab')

def main():
	for i in range(0, 5):
		pub1.publish('start')
		rospy.loginfo('start')
		rospy.sleep(1)

	rospy.Subscriber('dir', String, callback)
	rospy.spin()

if __name__ == '__main__':
	main()
