#!/usr/bin/env python

import os
import rospy
import serial
import argparse
from std_msgs.msg import String

parser = argparse.ArgumentParser()
parser.add_argument('-p', action='store', dest='port', help='Store port name', required=True, type=str)
args = parser.parse_args()

arduino = serial.Serial(args.port, 9600)
status_count = 5

rospy.init_node('arm',anonymous=True)
rate = rospy.Rate(10)

def callback(data):
	global status_count
	rospy.loginfo(rospy.get_caller_id() + "Arm Status: %s", data.data)
	if data.data == 'Grab':
		print 'Countdown: ' + str(status_count)
		if status_count <= 0:
			arduino.write("G")
			print "Grabbed"
			pass
		else:
			arduino.write("C")
			print "Counting"
			pass
		status_count = status_count - 1
	else:
		status_count = 5

def main():
	arduino.write("W")
	rospy.Subscriber('grab', String, callback)
	rospy.spin()

if __name__ == '__main__':
	main()
