from turtle import back, shape
import cv2 as cv
import cvzone as cz
from cvzone.HandTrackingModule import *

######################################################################################
#Setting Window
cap = cv.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)

Detector = HandDetector(maxHands=1)

background_img = cv.imread("E:/Extra Codes/Python/Python Projects/Virtual FunHub (Games)/InterFace/Images/welcome background/background_img1.png")
background_img2 = cv.imread("E:/Extra Codes/Python/Python Projects/Virtual FunHub (Games)/InterFace/Images/welcome background/background_img_2page.png")

count = 0
while True:
    SUCCESS, img = cap.read()
    img = cv.flip(img, 1)

    hand, img = Detector.findHands(img)

    img_first = cv.addWeighted(img, 0.12, background_img, 1, 0)



    ######################################################################################
    #Writing Text on the Screen
    cv.putText(img_first, 'Virtual FunHub', (478, 350), 0, 1.4, (255, 255, 255), 3)
    cv.putText(img_first, 'Wave your Hand to Start', (440, 650), 0, 1, (255, 255, 255), 3)
    cv.putText(img_first, 'Creators', (1165, 615), 0, 0.8, (255, 255, 255), 1)
    cv.line(img_first, (1165, 620), (1280,620), (255, 255, 255), 1)
    cv.putText(img_first, 'Vedant', (1180, 650), 0, 0.8, (255, 255, 255), 2)
    cv.putText(img_first, 'Manan', (1180, 679), 0, 0.8, (255, 255, 255), 2)
    cv.putText(img_first, 'Rinkesh', (1180, 708), 0, 0.8, (255, 255, 255), 2)
    ######################################################################################

    if hand:
        hand1 = hand[0]
        lmlist = hand1["lmList"]
        x1, y1 = lmlist[8][:2]
        fingers = Detector.fingersUp(hand1)

        if fingers == [1,1,1,1,1]:
            count += 1
            if count == 20:
                cv.destroyWindow("Image")
                img = background_img2
                recta = img.copy()
                cv.rectangle(recta, (0,0), (1280,720),(0,0,0),-1)
                img = cv.addWeighted(recta, 0.5, img, 0.5, 0)
                cv.putText(img, 'Loading...', (370, 350), 0, 4, (255, 255, 255), 4)
                cv.imshow("Image",img)
                cv.waitKey(1)
                print("Go to next Page")
                exec(open("E:/Extra Codes/Python/Python Projects/Virtual FunHub (Games)/InterFace/main.py").read())

    cv.imshow("Image",img_first)

    cv.waitKey(1)