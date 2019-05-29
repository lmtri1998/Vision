import cv2
import numpy as np
import argparse
import imutils

# construct arg parse

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
                help="path to the input image")
args = vars(ap.parse_args())

# load the image and resize it to a smaller factor so that
# the shapes can be approximated better
image = cv2.imread(args["image"])

hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

lower_red = np.array([30, 150, 50])
upper_red = np.array([255, 255, 180])

mask = cv2.inRange(hsv, lower_red, upper_red)
res = cv2.bitwise_and(image, image, mask=mask)

laplacian = cv2.Laplacian(image, cv2.CV_64F)
sobelx = cv2.Sobel(image, cv2.CV_64F, 1, 0, ksize=5)
sobely = cv2.Sobel(image, cv2.CV_64F, 0, 1, ksize=5)

cv2.imwrite('mask.png', mask)
cv2.imwrite('laplacian.png', laplacian)
cv2.imwrite('sobelx.png', sobelx)
cv2.imwrite('sobely.png', sobely)
cv2.imwrite('res.png', res)