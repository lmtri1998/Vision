import xmltodict
import cv2
import numpy as np
import imutils
import argparse
import glob

filename_img = "Images\\lethanhsang_warped.jpg"
filename_xml = "Annotations\\lethanhsang_warped.xml"


ap = argparse.ArgumentParser()
ap.add_argument("-i", "--images", required=True,
                help="path to the input images")
args = vars(ap.parse_args())


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
def crop_binarize_and_segment_image(img, part, path_xml, count):
    b = get_boxes(path_xml, part)
    img_x, img_y, img_w, img_h = get_dimensions(b)
    crop_img = img[img_y:img_y + img_h, img_x:img_x + img_w]
    gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
    # cv2.imwrite("test\\" + part + "_gray" + str(count) + ".png", gray)
    # blur = cv2.GaussianBlur(gray, (3, 3), 0)
    ret, th = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    # ret, th = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)
    th = 255 - th

    cnts = cv2.findContours(th.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    seg_dims = []

    num_c = 0
    for c in cnts:
        if cv2.contourArea(c) >= 5:
            x, y, w, h = cv2.boundingRect(c)
            x, y, w, h = x - 1, y - 1, w + 1, h + 1
            x = 0 if x - 1 <= 0 else x - 1
            y = 0 if y - 1 <= 0 else y - 1
            w = w if (w + x) >= (img_w + img_x) else w + 1
            h = h if (h + y) >= (img_h + img_y) else h + 1

            seg_dims.append([x, y, w, h])
            # cv2.rectangle(crop_img, (x, y), (x + w, y + h), (0, 255, 0), 1)
            # print(x, y, w, h)
            cv2.imwrite("test\\" + part + "_" + str(count) + "_" + str(num_c) + ".png", crop_img[y:y+h, x:x+w])
            num_c += 1
    return seg_dims


# img = cv2.imread(filename_img)
# print(crop_binarize_and_segment_image(img, "readable_1", filename_xml))
# print(crop_binarize_and_segment_image(img, "readable_2", filename_xml))

c = 0
for imagePath in glob.glob(args["images"] + "/*_warped.jpg"):
    filename = imagePath.split(".")
    name = filename[0].split("\\")
    xml_path = "Annotations\\" + name[1] + ".xml"

    img = cv2.imread(imagePath)
    crop_binarize_and_segment_image(img, "readable_1", xml_path, c)
    crop_binarize_and_segment_image(img, "readable_2", xml_path, c)
    c += 1
