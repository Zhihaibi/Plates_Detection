import cv2
import numpy as np


def Circle_extract(Image, Circle):
    Img_circle = np.copy(Image)
    Size = list(Image.shape)
    for i in range(Size[0]):
        for j in range(Size[1]):
            Distance = (j - Circle[0]) * (j - Circle[0]) + (i - Circle[1]) * (i - Circle[1])
            if Distance >= Circle[2] * Circle[2]:
                Img_circle[i][j] = 0
    return Img_circle


def Circle_detection(Img_gray):
    gaussian = cv2.GaussianBlur(Img_gray, (3, 3), 0)
    circles1 = cv2.HoughCircles(gaussian, cv2.HOUGH_GRADIENT, 1, 100, param1=100, param2=30, minRadius=100,
                                maxRadius=120)
    print(np.shape(circles1))  # hough_gradient
    circles = circles1[0, :, :]
    print(circles)
    circles = np.uint16(np.around(circles))

    for i in circles[:]:
        print('[x,y,radius] = ', i)
        print(type(i))
        # Img_circle = Circle_extract(img, i)
        # cv2.imshow('img', Img_circle)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        cv2.circle(img, (i[0], i[1]), i[2], (0, 0, 0), 3)  # line
        cv2.circle(img, (i[0], i[1]), 2, (0, 0, 0), 2 * i[2])  # center point


img = cv2.imread('D:/Users/bzh/Desktop/Image3.jpg')
Img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
Circle_detection(Img_gray)  # Hough circle detection

cv2.imshow('img', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
