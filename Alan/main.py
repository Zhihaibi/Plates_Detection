import cv2
import numpy as np


# 圆形检测，并涂上黑色
def Circle_detection(Image):
    Img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gaussian = cv2.GaussianBlur(Img_gray, (3, 3), 0)
    circles1 = cv2.HoughCircles(gaussian, cv2.HOUGH_GRADIENT, 1, 100, param1=100, param2=30, minRadius=100,maxRadius=120)
    print(np.shape(circles1))  # hough_gradient
    circles = circles1[0, :, :]
    print(circles)
    circles = np.uint16(np.around(circles))
    return circles


# 提取所有圆，返回圆心与半径
def Circle_extract(Image, Circle):
    Img_circle = np.copy(Image)
    Size = list(Image.shape)
    for i in range(Size[0]):
        for j in range(Size[1]):
            Distance = (j - Circle[0]) * (j - Circle[0]) + (i - Circle[1]) * (i - Circle[1])
            if Distance >= Circle[2] * Circle[2]:
                Img_circle[i][j] = 0
    return Img_circle


def FillHole(im_in):
    im_floodfill = im_in.copy()
    h, w = im_in.shape[:2]
    mask = np.zeros((h + 2, w + 2), np.uint8)
    isbreak = False
    for i in range(im_floodfill.shape[0]):
        for j in range(im_floodfill.shape[1]):
            if (im_floodfill[i][j] == 0):
                seedPoint = (i, j)
                isbreak = True
                break
        if (isbreak):
            break
    cv2.floodFill(im_floodfill, mask, seedPoint, 255);
    im_floodfill_inv = cv2.bitwise_not(im_floodfill)
    fillhole = im_in | im_floodfill_inv
    return fillhole


#=====================================================================#
######################## Test ########################################

img = cv2.imread('images/Image3.jpg')
img_backup = np.copy(img)
img = cv2.GaussianBlur(img, (3, 3), 0)
img_canny = cv2.Canny(img, 10, 160)

# Remove outer contour
image, contours, hier = cv2.findContours(img_canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_TC89_L1)
cv2.drawContours(image, contours, -1, (0, 0, 0), 2)

# Circles detect
Circles = Circle_detection(img_backup)
for i in Circles[:]:
    # Extract the circle and show
    Img_circle = Circle_extract(img_backup, i)
    cv2.imshow('img_backup', Img_circle)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # Remove the circle
    if i[2] >= 113:
        i[2] = 105
    print('[x,y,radius] = ', i)
    cv2.circle(image, (i[0], i[1]), i[2], (0, 0, 0), 3)  # Circle line
    cv2.circle(image, (i[0], i[1]), 2, (0, 0, 0), 2 * i[2])  # center point

kernel = np.ones((8, 8), np.uint8)
Img_closing = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)
Img_Hole = FillHole(Img_closing)
Img_erosion = cv2.erode(Img_Hole, kernel, iterations=2)

cv2.imshow("Img_rec", Img_erosion)
cv2.waitKey()
cv2.destroyAllWindows()