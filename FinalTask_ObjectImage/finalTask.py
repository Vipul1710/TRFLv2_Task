import cv2
from imutils import paths
import numpy as np
import imutils
import os

def find_marker(image):
	# converting the image to grayscale
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	# detecting the image
	gray = cv2.GaussianBlur(gray, (5, 5), 0)
	edged = cv2.Canny(gray, 35, 125)
	cv2.imshow('canny', edged)

	# finding the contour in image
	contours = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
	contours = imutils.grab_contours(contours)
	# finding the largest contour in image
	c = max(contours, key = cv2.contourArea)

	# returning the boundary box
	return cv2.minAreaRect(c)

def distance_to_camera(objWdth, fclLnth, perWdth):
	# calculating distance between camera and object
	return (objWdth * fclLnth) / perWdth

# object pre-defined distance from the camera
objDist = 30

# object pre-defined width
objWdth = 8.5

# reading pre-defined image
image = cv2.imread("images/1.jpg")
# finding contour in image
marker = find_marker(image)
# manipulating focal length through pre-defined data
fclLnth = (marker[1][0] * objDist) / objWdth
print('focal length : ', fclLnth)
lst = []
# accessing images from folder
for i in range(1, 100):
	if os.path.isfile('images/' + str(i) + '.jpeg'):
		lst.append(str(i) + '.jpeg')

# iterating through images and manipulating result
for imageName in lst:
	# reading images one after another
	image = cv2.imread('images/' + imageName)
	# getting contour
	marker = find_marker(image)
	# finding distance
	distInch = distance_to_camera(objWdth, fclLnth, marker[1][0])

	# drawing a box around the image
	box = cv2.cv.BoxPoints(marker) if imutils.is_cv2() else cv2.boxPoints(marker)
	box = np.int0(box)
	cv2.drawContours(image, [box], -1, (255, 255, 0), 3)
	# displaying output on image
	cv2.putText(image, "%.2f Inch" % (distInch), (80, 50), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 2, (255, 255, 255), 3)
	print("Image-", imageName,  ": %.2f Inch" % (distInch))
	cv2.imwrite('result/image-' + imageName, image)
	# full-screen window
	cv2.namedWindow('image- ' + imageName, cv2.WND_PROP_FULLSCREEN)
	cv2.setWindowProperty('image- ' + imageName, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
	# displaying image
	cv2.imshow("image- " + imageName, image)
	cv2.waitKey(0)