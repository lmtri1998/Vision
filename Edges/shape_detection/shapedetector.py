import cv2


class ShapeDetector:
    def __init__(self):
        pass

    def detect(self, c):
        # initialize the shape name and approx. the contour
        shape = "unidentified"
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.04 * peri, True)

        # if the shape is triangle, it will have 3 vertices
        if len(approx) == 3:
            shape = "triangle"
        # if the shape has for vertices, it is either a square
        # or rectangle.
        elif len(approx) == 4:
            # find the bounding rect.
            (x, y, w, h) = cv2.boundingRect(approx)
            # ar is aspect ratio.
            ar = w / float(h)

            # a square will have an aspect ratio that is approx.
            # equal to one, otherwise, the shape is a rectangle
            shape = "square" if 0.95 <= ar <= 1.05 else "rectangle"
        elif len(approx) == 5:
            shape = "pentagon"
        else:
            shape = "circle"
        return shape

