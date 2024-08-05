import cv2
from object_detector import *
import numpy as np

# Load Aruco detector
parameters = cv2.aruco.DetectorParameters()
aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_7X7_100)


# Load Object Detector
detector = HomogeneousBgDetector()

# Load Image
#img = cv2.imread("phone_aruco_marker.jpg")
img = cv2.imread("IMG20240527211556.jpg")

# Get Aruco marker
corners, _, _ = cv2.aruco.detectMarkers(img, aruco_dict, parameters=parameters)

# Draw polygon around the marker
int_corners = np.intp(corners)
#cv2.polylines(img, int_corners, True, (0, 255, 0), 5)

# Aruco Perimeter
aruco_perimeter = cv2.arcLength(corners[0], True)

#print("Aruco Parimter: ", aruco_perimeter)

# Pixel to cm ratio
pixel_cm_ratio = aruco_perimeter / 40

#print("Pixel to CM Ratio: ", pixel_cm_ratio)

contours = detector.detect_objects(img)

# Draw objects boundaries
for cnt in contours:
    # Get rect
    rect = cv2.minAreaRect(cnt)
    (x, y), (w, h), angle = rect
    
    # print("Detected Width: ", w)
    # print("Detected Height: ", h)

    # Get Width and Height of the Objects by applying the Ratio pixel to cm
    object_width = w / pixel_cm_ratio
    object_height = h / pixel_cm_ratio
    
    print("Width: ", object_width)
    print("Height: ", object_height)

    # Display rectangle
    box = cv2.boxPoints(rect)
    box = np.intp(box)

    cv2.circle(img, (int(x), int(y)), 5, (0, 0, 255), -1)
    cv2.polylines(img, [box], True, (255, 0, 0), 2)
    cv2.putText(img, "Width {} cm".format(round(object_width, 1)), (int(x - 100), int(y - 20)), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
    cv2.putText(img, "Height {} cm".format(round(object_height, 1)), (int(x - 100), int(y + 15)), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)


img = cv2.resize(img,(400, 800),None,0.5,0.5)
cv2.imshow("Image", img)
cv2.waitKey(0)