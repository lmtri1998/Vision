import xmltodict
import cv2
import numpy as np
import imutils


filename_img = "Images\\dinhvantao_warped.jpg"
filename_xml = "Annotations\\dinhvantao_warped.xml"


# get points from an xml file
def get_boxes(path, name):
    with open(path) as fd:
        doc = xmltodict.parse(fd.read())
    points = []
    for obj in doc['annotation']['object']:
        if name in obj['name']:
            for pt in obj['polygon']['pt']:
                points.append([int(pt['x']), int(pt['y'])])

    return np.array(points)


# get the dimensions of the cropped img box
def get_dimensions(box):
    top_left_x = min(int(box[0][0]), int(box[1][0]), int(box[2, 0]), int(box[3, 0]))
    top_left_y = min(int(box[0][1]), int(box[1][1]), int(box[2, 1]), int(box[3, 1]))
    btm_right_x = max(int(box[0][0]), int(box[1][0]), int(box[2, 0]), int(box[3, 0]))
    btm_right_y = max(int(box[0][1]), int(box[1][1]), int(box[2, 1]), int(box[3, 1]))
    width = btm_right_x - top_left_x
    height = btm_right_y - top_left_y
    return top_left_x, top_left_y, width, height


# binarize the image
def crop_binarize_and_segment_image(img, part, path_xml):
    b = get_boxes(path_xml, part)
    x, y, w, h = get_dimensions(b)
    crop_img = img[y:y + h, x:x + w]

    gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
    # ret, th = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    ret, th = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    th = 255 - th

    cnts = cv2.findContours(th.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    count = 0
    seg_dims = []

    for c in cnts:
        x, y, w, h = cv2.boundingRect(c)
        seg_dims.append([x, y, w, h])
        count += 1
    return seg_dims


img = cv2.imread(filename_img)
print(crop_binarize_and_segment_image(img, "readable_1", filename_xml))
print(crop_binarize_and_segment_image(img, "readable_2", filename_xml))

