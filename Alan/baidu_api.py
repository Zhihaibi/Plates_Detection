# encoding:utf-8
'''
Created on April 25th, 2020

@author: Alanby zhihaibi90@gmail.com
'''

#================================
#Trian on the baidu Api and test.
#================================

import requests
import base64
import json
import cv2


def Cv2_base64(image):
    base64_str = cv2.imencode('.jpg', image)[1].tostring()
    base64_str = base64.b64encode(base64_str)
    return base64_str


def read_img(img1, img2):
    with open(img1, 'rb') as f:
        pic1 = base64.b64encode(f.read())
    with open(img2, 'rb') as f:
        pic2 = base64.b64encode(f.read())
    params = json.dumps([
        {"image": str(pic1, "utf-8"), "image_type": 'BASE64', "face_type": "LIVE"},
        {"image": str(pic2, "utf-8"), "image_type": 'BASE64', "face_type": "LIVE"}
    ])
    return params


def Get_face_compare_result(Aim_img):
    # Get access_token
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=4xSj383NDzbV5GgEFiwCsjAB&client_secret=WMlKSlaBMQrXKK8tFnHENegyrXcfhmi3'
    response = requests.get(host)
    if response:
        json1 = response.json()  # <class 'dict'>
        access_token = json1['access_token']
    else:
        print('Get access_token fail!')
        return -1
    # Compare two picture
    img1 = Cv2_base64(Aim_img)
    params = json.dumps(
        {"image": str(img1, "utf-8"), "threshold": 0.3}
    )
    request_url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/segmentation/plate_test_v2"
    request_url = request_url + "?access_token=" + access_token
    headers = {'content-type': 'application/json'}
    response = requests.post(request_url, data=params, headers=headers)

    if response:
        result = response.json()['results']
        return result
    else:
        return -1

        length = len(face_compare_score)
        for i in range(length):
            print(face_compare_score[i]['name'])
            print(face_compare_score[i]['location'])


img = cv2.imread('D:/Users/bzh/Desktop/Image3.jpg')
result = Get_face_compare_result(img)
if result != -1:
    length = len(result)
    for i in range(length):
        name = result[i]['name']
        left = result[i]['location']['left']
        top = result[i]['location']['top']
        right = left + result[i]['location']['width']
        bottom = top + result[i]['location']['height']

        draw_image = cv2.rectangle(img, (left, top), (right, bottom), (0, 0, 255), 2)
        cv2.putText(draw_image, str(i + 1) + ' ' + name, (left, bottom), cv2.FONT_HERSHEY_TRIPLEX, 0.6, (0, 255, 0), 1)
        cv2.imshow('img', img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
