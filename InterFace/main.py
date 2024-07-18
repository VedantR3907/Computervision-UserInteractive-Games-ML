import cvzone as cz
import cv2 as cv
from cvzone.HandTrackingModule import *
Detector = HandDetector(maxHands=1)

background_img_balloon_pop = cv.imread("E:/Extra Codes/Python/Python Projects/Virtual FunHub (Games)/InterFace/Images/balloon pop/bp1.png")
background_img_rps = cv.imread("E:/Extra Codes/Python/Python Projects/Virtual FunHub (Games)/InterFace/Images/Rock Paper Scissor/rpsgame2.png")
background_img_pg = cv.imread("E:/Extra Codes/Python/Python Projects/Virtual FunHub (Games)/InterFace/Images/Pong Game/p2.png")
background_img_sg = cv.imread("E:/Extra Codes/Python/Python Projects/Virtual FunHub (Games)/InterFace/Images/Snake Game/s2.png")
background_img_ern = cv.imread("E:/Extra Codes/Python/Python Projects/Virtual FunHub (Games)/InterFace/Images/Eat or Not/ern1.png")
background_img_vq = cv.imread("E:/Extra Codes/Python/Python Projects/Virtual FunHub (Games)/InterFace/Images/Virtual Quiz/vq2.png")

img_balloon_pop_main = cv.imread("E:/Extra Codes/Python/Python Projects/Virtual FunHub (Games)/InterFace/Images/balloon pop/bp2_crop.png")
img_rps_main = cv.imread("E:/Extra Codes/Python/Python Projects/Virtual FunHub (Games)/InterFace/Images/Rock Paper Scissor/rpsgame2_crop.png")
img_pg_main = cv.imread("E:/Extra Codes/Python/Python Projects/Virtual FunHub (Games)/InterFace/Images/Pong Game/p2_crop.png")
img_sg_main = cv.imread("E:/Extra Codes/Python/Python Projects/Virtual FunHub (Games)/InterFace/Images/Snake Game/s2_crop.png")
img_ern_main = cv.imread("E:/Extra Codes/Python/Python Projects/Virtual FunHub (Games)/InterFace/Images/Eat or Not/ern1_crop.png")
img_vq_main = cv.imread("E:/Extra Codes/Python/Python Projects/Virtual FunHub (Games)/InterFace/Images/Virtual Quiz/vq2_crop.png")
######################################################################################
#Setting Window
cap = cv.VideoCapture(0, cv2.CAP_DSHOW) # this is the magic!

cap.set(cv.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv.CAP_PROP_FRAME_HEIGHT, 1080)
flag = 0

while True:
    SUCCESS, img = cap.read()
    img = cv.flip(img, 1)

    hand, img = Detector.findHands(img)
    if hand:
        hand1 = hand[0]
        lmlist = hand1["lmList"]
        x1, y1 = lmlist[8][:2]
        fingers = Detector.fingersUp(hand1)
        print(x1,y1)
        if fingers[1] and fingers[2]:  #Both Fingers UP

            #Snake Game
            if 115<=x1<=315 and 115<=y1<=315:
                flag = 1
                cv.destroyWindow("Image")
                img = background_img_sg
                cv.imshow("Image",img)
                cv.waitKey(1)
                print("Go to next Page")
            if 100<=x1<=300 and 100<=y1<=300:
                exec(open("E:/Extra Codes/Python/Python Projects/Virtual FunHub (Games)/Snake Game/main.py").read())
            
    if flag == 0:
        img[100:300,100:300] = img_sg_main
        img[100:300,500:700] = img_rps_main
        img[100:300,900:1100] = img_pg_main
        img[400:600,100:300] = img_balloon_pop_main
        img[400:600,500:700] = img_vq_main
        img[400:600,900:1100] = img_ern_main
    cv.imshow("Image", img)
    cv.waitKey(1)