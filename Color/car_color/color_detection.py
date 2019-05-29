import numpy as np
import argparse
import cv2
import imutils
from sklearn.cluster import MiniBatchKMeans
import time


def unique_count_app(a):
    colors, count = np.unique(a.reshape(-1, a.shape[-1]), axis=0, return_counts=True)
    return colors[count.argmax()]


def bincount_app(a):
    a2D = a.reshape(-1,a.shape[-1])
    col_range = (256, 256, 256) # generically : a2D.max(0)+1
    a1D = np.ravel_multi_index(a2D.T, col_range)
    return np.unravel_index(np.bincount(a1D).argmax(), col_range)

# def make_histogram(cluster):
#     """
#     Count the number of pixels in each cluster
#     :param: KMeans cluster
#     :return: numpy histogram
#     """
#     numLabels = np.arange(0, len(np.unique(cluster.labels_)) + 1)
#     hist, _ = np.histogram(cluster.labels_, bins=numLabels)
#     hist = hist.astype('float32')
#     hist /= hist.sum()
#     return hist


start = time.time()
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="path to the image file")
args = vars(ap.parse_args())

# load the image.
image = cv2.imread(args["image"])
image = imutils.resize(image, width=300)
blurred = cv2.GaussianBlur(image, (11, 11), 0)
gray = cv2.cvtColor(blurred, cv2.COLOR_BGR2GRAY)

mask = cv2.erode(gray, None, iterations=2)
mask = cv2.dilate(mask, None, iterations=2)
thresh = cv2.threshold(mask, 75, 255, cv2.THRESH_BINARY)[1]

# gray = cv2.bilateralFilter(gray, 11, 17, 17)
cv2.imwrite("12.jpg", mask)

cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)

if len(cnts) > 0:
    c = max(cnts, key=cv2.contourArea)
    x, y, w, h = cv2.boundingRect(c)
    new_img = image[y:y + h, x:x + w]
    color = bincount_app(image)
    print(color)
    new_img = new_img.reshape((new_img.shape[0] * new_img.shape[1], 3))
    cluster = MiniBatchKMeans(init='k-means++', max_iter=300, n_clusters=1,
                              random_state=0, tol=0.0001, verbose=0)
    cluster.fit_predict(new_img)
    print(cluster.cluster_centers_)

    img = np.zeros((512, 512, 3), np.uint8)
    cv2.line(img, (128, 0), (128, 511),
             (int(cluster.cluster_centers_[0][0]), int(cluster.cluster_centers_[0][1]),
             int(cluster.cluster_centers_[0][2])), 254)
    cv2.line(img, (384, 0), (384, 511), (int(color[0]), int(color[1]), int(color[2])), 254)

    stop = time.time()
    cv2.imwrite("color.jpg", img)
    print("processing time: ", stop - start)





