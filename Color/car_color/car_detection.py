import argparse
import cv2
import imutils
import operator
import time

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="path to the image file")
args = vars(ap.parse_args())

# define the lower and upper boundaries of the colors in the HSV color space
lower = {'red': (166, 84, 141), 'green': (66, 122, 129), 'blue': (97, 100, 117), 'yellow': (23, 59, 119),
         'orange': (0, 50, 80), 'black': (0, 0, 0), 'white': (0, 0, 215), 'gray': (0, 0, 88),
         'silver': (0, 0, 152)}
upper = {'red': (186, 255, 255), 'green': (86, 255, 255), 'blue': (117, 255, 255), 'yellow': (54, 255, 255),
         'orange': (20, 255, 255),  'black': (10, 40, 40), 'white': (10, 40, 295), 'gray': (10, 40, 168),
         'silver': (10, 40, 232)}

# define standard colors for circle around the object
colors = {'red': (0, 0, 255), 'green': (0, 255, 0), 'blue': (255, 0, 0), 'yellow': (0, 255, 217),
          'orange': (0, 140, 255), 'black': (0, 0, 0), 'white': (255, 255, 255), 'gray': (128, 128, 128),
          'silver': (192, 192, 192)}

result = {}

img = cv2.imread(args["image"])
img = imutils.resize(img, width=300)
blurred = cv2.GaussianBlur(img, (11, 11), 0)
hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
start = time.time()
for key, val in colors.items():
    mask = cv2.inRange(hsv, lower[key], upper[key])
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    # find contours in the mask
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    if len(cnts) > 0:
        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        if radius > 0.5:
            result[key] = radius
stop = time.time()

print(max(result.items(), key=operator.itemgetter(1))[0])
print("processing time:", stop - start)