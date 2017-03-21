'''
Makeathon National Instruments Autonomous Vehicle Challenge
Visual Traffic Signal and Sign Recognition
'''


#!/usr/bin/env python
import sys
import time
from array import array
import numpy as np
import argparse
import imutils
import sys

sys.path.append('/usr/local/lib/python2.7/site-packages')
import cv2

import argparse
import time
import glob

class Vision(object):
	"""docstring for Vision."""
	cap = None
	show_mode = False
	current_ret = None
	current_frame = None
	blob_detector = None
	blob_params = None

	prototypeImg = cv2.imread("./stopPrototype.png")


	def __init__(self):
		super(Vision, self).__init__()
		# Blob Detector Parameters:
		self.blob_params = cv2.SimpleBlobDetector_Params()

		# Change thresholds
		self.blob_params.minThreshold = 10
		self.blob_params.maxThreshold = 200


		# Filter by Area.
		self.blob_params.filterByArea = True
		self.blob_params.minArea = 500

		# Filter by Circularity
		self.blob_params.filterByCircularity = True
		self.blob_params.minCircularity = 0.80

		# Filter by Convexity
		self.blob_params.filterByConvexity = True
		self.blob_params.minConvexity = 0.80

		# Filter by Inertia
		self.blob_params.filterByInertia = True
		self.blob_params.minInertiaRatio = 0.01

		# Create a detector with the parameters
		ver = (cv2.__version__).split('.')
		if int(ver[0]) < 3 :
			self.blob_detector = cv2.SimpleBlobDetector(self.blob_params)
		else :
			self.blob_detector = cv2.SimpleBlobDetector_create(self.blob_params)

	def __del__(self):
		# When everything done, release the capture
		self.cap.release()
		cv2.destroyAllWindows()

	def connect(self):
		# Connect to PS3 Eye:
		print("Connection to camera")
		self.cap = cv2.VideoCapture(1)
		print("Connection Established")

	def check_sign(self):
		print("Checking Sign")
		if self.current_ret == False:
			self.connect()
		# Read:
		self.current_ret, self.current_frame = self.cap.read(1)
		self.current_frame = cv2.medianBlur(self.current_frame, 5)
		# Detect blobs.
		keypoints = self.blob_detector.detect(self.current_frame)

		# Draw detected blobs as red circles.
		# cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures
		# the size of the circle corresponds to the size of blob
		print(keypoints)
		im_with_keypoints = cv2.drawKeypoints(self.current_frame, keypoints, np.array([]), (0,255,0), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

		# Show blobs
		cv2.imshow("Keypoints", im_with_keypoints)
		cv2.waitKey(0)

		# Show:
		if self.show_mode:
			cv2.imshow('current_frame', self.current_frame)
			waitKey(0)



	def check_light(self):
		#
		i = 1

	def set_show(self, arg):
		show_mode = arg


v = Vision()
v.connect()
v.set_show(True)
v.check_sign()

destroyAllWindows()
