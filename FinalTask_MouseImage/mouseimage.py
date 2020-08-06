import cv2
from imutils import paths
import numpy as np
import imutils
import os


lr = np.array([170, 120, 70])
hr = np.array([180, 255, 255])

ly =np.array([12, 93, 90])
hy =np.array([45, 255, 255])

#click event function
def click_event(event, x, y, flags, param):
    lstImg = []
    for i in range(1, 100):
        if os.path.isfile('images/r' + str(i) + '.jpeg'):
            lstImg.append('images/r' + str(i) + '.jpeg')
    # print(lstImg)
    for i in lstImg:
        image = cv2.imread(i)
        if event == cv2.EVENT_LBUTTONDOWN:
            marker = find_marker(image)
            # finding distance
            distInch = distance_to_camera(objWdth, fclLnth, marker[1][0])
            # drawing a box around the image
            box = cv2.cv.BoxPoints(marker) if imutils.is_cv2() else cv2.boxPoints(marker)
            box = np.int0(box)
            cv2.drawContours(image, [box], -1, (255, 255, 0), 3)
            # displaying output on image
            cv2.putText(image, "%.2f Inch" % (distInch), (80, 50), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 2, (255, 255, 0), 3)
            image = cv2.resize(image, (500, 500))
            print("Image-" + i, ": %.2f Inch" % (distInch))
            cv2.imshow(i, image)

    lstImgY = []
    for i in range(1, 100):
        if os.path.isfile('images/y' + str(i) + '.jpeg'):
            lstImgY.append('images/y' + str(i) + '.jpeg')
    # print(lstImgY)
    for i in lstImgY:
        imageY = cv2.imread(i)
        if event == cv2.EVENT_RBUTTONDOWN:
            markerY = find_markerY(imageY)
            # finding distance
            distInch = distance_to_camera(objWdth, fclLnthY, markerY[1][0])
            # drawing a box around the image
            box = cv2.cv.BoxPoints(markerY) if imutils.is_cv2() else cv2.boxPoints(markerY)
            box = np.int0(box)
            cv2.drawContours(imageY, [box], -1, (255, 255, 0), 3)
            # displaying output on image
            cv2.putText(imageY, "%.2f Inch" % (distInch), (80, 50), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 2, (255, 255, 0), 3)
            print("Image-" + i, ": %.2f Inch" % (distInch))
            cv2.imshow(i, imageY)


def distance_to_camera(objWdth, fclLnth, perWdth):
	# calculating distance between camera and object
	return (objWdth * fclLnth) / perWdth

def find_marker(image):
	# converting the image to grayscale
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
	# COLOR MASKING
	mask = cv2.inRange(gray, lr, hr)  # masking so as to be more efficient
	edged = cv2.Canny(mask, 35, 125)
	# cv2.imshow('canny', edged)

	# finding the contour in image
	contours = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
	contours = imutils.grab_contours(contours)
	# finding the largest contour in image
	c = max(contours, key = cv2.contourArea)

	# returning the boundary box
	return cv2.minAreaRect(c)


def find_markerY(imageY):
	# converting the image to grayscale
	gray = cv2.cvtColor(imageY, cv2.COLOR_BGR2HSV)
	# COLOR MASKING
	mask = cv2.inRange(gray, ly, hy)  # masking so as to be more efficient
	edged = cv2.Canny(mask, 35, 125)
	# cv2.imshow('canny', edged)

	# finding the contour in image
	contours = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
	contours = imutils.grab_contours(contours)
	# finding the largest contour in image
	c = max(contours, key = cv2.contourArea)

	# returning the boundary box
	return cv2.minAreaRect(c)

objDist = 30
objWdth = 2.3

image = cv2.imread('images/r1.jpeg')
marker = find_marker(image)
fclLnth = (marker[1][0] * objDist) / objWdth

imageY = cv2.imread("images/y1.jpeg")
markerY = find_markerY(imageY)
fclLnthY = (markerY[1][0] * objDist) / objWdth

cv2.imshow("image", image)

#calling the mouse click event
cv2.setMouseCallback("image", click_event)

cv2.waitKey(0)
cv2.destroyAllWindows()