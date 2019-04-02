import cv2
import numpy as np

_DILATE_KERNEL = np.array([[0, 1, 0],
                           [1, 1, 1],
                           [0, 1, 0]], dtype=np.uint8)
def dilate(img):
    dilate = cv2.dilate(img,_DILATE_KERNEL)
    return dilate
def eroded(img):
    eroded = cv2.erode(img,_DILATE_KERNEL)
    return eroded

def run():
    img = cv2.imread('/home/tim/Desktop/anjuke_template.jpg')
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    _, mask = cv2.threshold(gray, 0, 255, cv2.THRESH_TOZERO + cv2.THRESH_OTSU)
    _, mask = cv2.threshold(mask, 127, 255, cv2.THRESH_BINARY)

    #mask = dilate(mask)

    img = cv2.bitwise_and(img,img,mask)
    mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
    cv2.imshow('img',img)
    cv2.imshow('mask',mask)
    cv2.imwrite('/home/tim/Desktop/template.png',mask)
    cv2.waitKey(0)

def find():
    gray_img = cv2.imread('/home/tim/Desktop/ceshi,jpg',0)
    cv2.waitKey(0)


if __name__ == "__main__":

    run()




