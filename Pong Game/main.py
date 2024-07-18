import cv2
import numpy as np
import cvzone
from cvzone.HandTrackingModule import HandDetector

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

# Importing all images
imgBackground = cv2.imread("E:/Extra Codes/Python/Python Projects/Virtual FunHub (Games)/Pong Game/Images/Background.png")
imgGameOver = cv2.imread("E:/Extra Codes/Python/Python Projects/Virtual FunHub (Games)/Pong Game/Images/gameOver.png")
imgBall = cv2.imread("E:/Extra Codes/Python/Python Projects/Virtual FunHub (Games)/Pong Game/Images/Ball.png", cv2.IMREAD_UNCHANGED)
imgBall2 = cv2.imread("E:/Extra Codes/Python/Python Projects/Virtual FunHub (Games)/Pong Game/Images/Ball.png", cv2.IMREAD_UNCHANGED)
imgBat1 = cv2.imread("E:/Extra Codes/Python/Python Projects/Virtual FunHub (Games)/Pong Game/Images/bat1.png", cv2.IMREAD_UNCHANGED)
imgBat2 = cv2.imread("E:/Extra Codes/Python/Python Projects/Virtual FunHub (Games)/Pong Game/Images/bat2.png", cv2.IMREAD_UNCHANGED)

# Hand Detector
detector = HandDetector(detectionCon=0.8, maxHands=2)

# Variables
ballPos = [100, 100]
ball2Pos = [500, 500]
speedX = 15
speedY = 15
speed2X = 20
speed2Y = 20
gameOver = False
score = [0, 0]
flag = 0

while True:
    _, img = cap.read()
    img = cv2.flip(img, 1)
    imgRaw = img.copy()

    # Find the hand and its landmarks
    hands, img = detector.findHands(img, flipType=False)  # with draw

    # Overlaying the background image
    img = cv2.addWeighted(img, 0.2, imgBackground, 0.8, 0)

    # Check for hands
    if hands:
        for hand in hands:
            x, y, w, h = hand['bbox']
            h1, w1, _ = imgBat1.shape
            y1 = y - h1 // 2
            y1 = np.clip(y1, 20, 415)

            if hand['type'] == "Left":
                img = cvzone.overlayPNG(img, imgBat1, (59, y1))
                if 59 < ballPos[0] < 59 + w1 and y1 < ballPos[1] < y1 + h1:
                    speedX = -speedX
                    ballPos[0] += 30
                    score[0] += 1
                if 59 < ball2Pos[0] < 59 + w1 and y1 < ball2Pos[1] < y1 + h1:
                    speed2X = -speed2X
                    ball2Pos[0] += 30
                    score[0] += 1

            if hand['type'] == "Right":
                img = cvzone.overlayPNG(img, imgBat2, (1195, y1))
                if 1195 - 50 < ballPos[0] < 1195 and y1 < ballPos[1] < y1 + h1:
                    speedX = -speedX
                    ballPos[0] -= 30
                    score[1] += 1
                
                if 1195 - 50 < ball2Pos[0] < 1195 and y1 < ball2Pos[1] < y1 + h1:
                    speed2X = -speed2X
                    ball2Pos[0] -= 30
                    score[1] += 1

    # Game Over
    if ballPos[0] < 40 or ballPos[0] > 1200 or ball2Pos[0]<40 or ball2Pos[0] > 1200:
        gameOver = True

    if gameOver:
        img = imgGameOver
        cv2.putText(img, str(score[1] + score[0]).zfill(2), (585, 360), cv2.FONT_HERSHEY_COMPLEX,
                    2.5, (200, 0, 200), 5)
        cv2.putText(img, "Press Q to Quit", (400, 650),cv2.FONT_HERSHEY_COMPLEX, 2,(0, 0, 255), 5)

    # If game not over move the ball
    else:

        # Move the Ball
        if ballPos[1] >= 500 or ballPos[1] <= 10:
            speedY = -speedY

        ballPos[0] += speedX
        ballPos[1] += speedY

        if ball2Pos[1] >= 500 or ball2Pos[1] <= 10:
            speed2Y = -speed2Y

        ball2Pos[0] += speed2X
        ball2Pos[1] += speed2Y

        # Draw the ball
        img = cvzone.overlayPNG(img, imgBall, ballPos)
        img = cvzone.overlayPNG(img,imgBall2, ball2Pos)

        cv2.putText(img, str(score[0]), (300, 650), cv2.FONT_HERSHEY_COMPLEX, 3, (255, 255, 255), 5)
        cv2.putText(img, str(score[1]), (900, 650), cv2.FONT_HERSHEY_COMPLEX, 3, (255, 255, 255), 5)

    img[580:700, 20:233] = cv2.resize(imgRaw, (213, 120))
    hand, img = detector.findHands(img)
    cv2.imshow("Image", img)
    key = cv2.waitKey(1)
    
    if key == ord('r'):
        ballPos = [100, 100]
        ball2Pos = [500,500]
        speedX = 15
        speedY = 15
        speed2X = 20
        speed2Y = 20
        gameOver = False
        score = [0, 0]

    if key == ord('q'):
        cv2.destroyWindow("Image")
        img[:] = (0, 0, 0)
        cv2.putText(img, 'Loading...', (300, 400), cv2.FONT_HERSHEY_SIMPLEX, 5, (0, 0, 255), 5)
        cv2.imshow("Image",img)
        cv2.waitKey(1)
        exec(open("E:/Extra Codes/Python/Python Projects/Virtual FunHub (Games)/InterFace/main.py").read())
    imgGameOver = cv2.imread("E:/Extra Codes/Python/Python Projects/Virtual FunHub (Games)/Pong Game/Images/gameOver.png")