import cv2
from imutils import paths
import numpy as np
import imutils

def distance_to_camera(objWdth, fclLnth, perWdth):
	# calculating distance between camera and object
	return (objWdth * fclLnth) / perWdth

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

objDist = 20

objWdth = 6.5
images = cv2.imread("images/1.jpeg")
gray = cv2.cvtColor(images, cv2.COLOR_BGR2GRAY)
faces = face_cascade.detectMultiScale(gray, 1.2, 5)
for (x, y, w, h) in faces:
    cv2.rectangle(images, (x, y), (x + w, y + h), (255, 0, 0), 2)
cv2.imshow('Initial image', images)
fclLnth = (w * objDist) / objWdth

cap = cv2.VideoCapture(0)
while True:
    ret, image = cap.read(0)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=3)
    for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x+w, y+h), (255, 0, 0), 2)
    # finding distance
    distInch = distance_to_camera(objWdth, fclLnth, w)
    # displaying output on image
    cv2.putText(image, "%.2f Inch" % (distInch), (80, 50), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 2, (255, 255, 255), 3)
    print("Image-" + ": %.2f Inch" % (distInch))
    # full-screen window
    cv2.namedWindow('image- ', cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty('image- ', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    # displaying image

    cv2.imshow("image", image)

    k = cv2.waitKey(1)
    if (k == ord('q')):
        break

cap.release()
cv2.destroyAllWindows()


