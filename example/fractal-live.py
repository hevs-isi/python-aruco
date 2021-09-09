#/usr/bin/env python3
import cv2
import os
import sys
import cv2
import numpy as np
import aruco

print("aruco-python version {}".format(aruco.__version__))

cap = cv2.VideoCapture(1)
# Check if the webcam is opened correctly
if not cap.isOpened():
    raise IOError("Cannot open webcam")

width = 640
height = 480
cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
cap.set(cv2.CAP_PROP_AUTOFOCUS, 0)
# create fractaldetector and set config
detector = aruco.FractalDetector()
# set detector config first or it will throw an exception
detector.setConfiguration("FRACTAL_5L_6")

# load camera parameters
camparam = aruco.CameraParameters()


camparam.readFromXMLFile(filePath=os.path.join(os.path.dirname(__file__), "c525.yml"))

if camparam.isValid():
    print("valid")
    detector.setParams(camparam, 0.25)

while True:
    ret, frame = cap.read()
    #frame = cv2.resize(frame, None, fx=1.0, fy=1.0, interpolation=cv2.INTER_AREA)
    detected = detector.detect(frame)

    if detected:
        detector.drawMarkers(frame)
        markers = detector.getMarkers()
        # print id and points
        if 0:
        #for marker in markers:
            # print marker ID and point positions
            print("Marker: {:d}".format(marker.id))
            for i, point in enumerate(marker):
                print("\t{:d} {}".format(i, str(point)))
            marker.draw(frame, np.array([255, 255, 255]), 2)

        print("detected ids: {}".format(", ".join(str(m.id) for m in markers)))
        # draw fractal marker using detector
        detector.draw2d(frame)

    # get Pose and draw axis/cube
    if detector.poseEstimation():
        tvec = detector.getTvec()
        rvec = detector.getRvec()
        print("TVec:\n{}\nR:\n{}".format(tvec, rvec))
        # draw cube
        detector.draw3d(frame)

    cv2.imshow('Input', frame)

    c = cv2.waitKey(1)
    if c == 27:
        break

cap.release()
cv2.destroyAllWindows()
