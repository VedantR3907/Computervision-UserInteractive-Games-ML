# importing
import pygame
import cv2 as cv
import numpy as np
import random
from cvzone.HandTrackingModule import HandDetector
import time

def goingback():
    cv.destroyAllWindows()
    return 1

######################################################################################
#intialize
pygame.init()
video = cv.VideoCapture(0, cv.CAP_DSHOW)
codec = 0x47504A4D  # MJPG
video.set(cv.CAP_PROP_FPS, 30.0)
video.set(cv.CAP_PROP_FOURCC, codec)
video.set(cv.CAP_PROP_FRAME_WIDTH, 1920)
video.set(cv.CAP_PROP_FRAME_HEIGHT, 1080)

######################################################################################
#Setting Window
width, height = 1280,720
window = pygame.display.set_mode((width,height))
pygame.display.set_caption("Ballon Pop")

######################################################################################
#Initialize FPS
fps = 30
clock = pygame.time.Clock()

######################################################################################
#Images
ImgBalloon = pygame.image.load('E:/Extra Codes/Python/Python Projects/Virtual FunHub (Games)/Ballon Pop (Pygame)/Images_Project/BalloonRed.png').convert_alpha()

ImgBalloon_2 = pygame.image.load('E:/Extra Codes/Python/Python Projects/Virtual FunHub (Games)/Ballon Pop (Pygame)/Images_Project/BalloonBlue.png').convert_alpha()
ImgBalloon_2 = pygame.transform.scale(ImgBalloon_2,(115,200))

ImgBalloon_3 = pygame.image.load('E:/Extra Codes/Python/Python Projects/Virtual FunHub (Games)/Ballon Pop (Pygame)/Images_Project/BalloonMultiColor.png').convert_alpha()
ImgBalloon_3 = pygame.transform.scale(ImgBalloon_3,(200,250))

ImgPop = pygame.image.load('E:/Extra Codes/Python/Python Projects/Virtual FunHub (Games)/Ballon Pop (Pygame)/Images_Project/Pop.png').convert_alpha()
ImgPop = pygame.transform.scale(ImgPop,(200,200))

BalloonRect = ImgBalloon.get_rect()         #Creating Recctangle for Contact of hand and Image
BalloonRect.x, BalloonRect.y = 500, 500
BalloonRect_2 = ImgBalloon_2.get_rect()
BalloonRect_2.x, BalloonRect_2.y = 100, 700
BalloonRect_3 = ImgBalloon_3.get_rect()
BalloonRect_3.x, BalloonRect_3.y = 200, 200

######################################################################################
#Variables
Speed = 5
Speed_2 = 5
Speed_3 = 5
Score = 0
StartTime = time.time()
TotalTime = 50
CountBlueBalloon = 0
flag_for_exit_previous_window = 0

detector = HandDetector(detectionCon=0.8, maxHands=2)



def ResetBalloon():           #Used to randomly make balloon appear at places and Moving it Upside
    BalloonRect.x = random.randint(100,image.shape[1]-100)
    BalloonRect.y = image.shape[0]+50

def ResetBalloon_2():
    BalloonRect_2.x = random.randint(200,image.shape[1]-500)
    BalloonRect_2.y = image.shape[0]+75

def ResetBalloon_3():
    BalloonRect_3.x = random.randint(300,image.shape[1]-300)
    BalloonRect_3.y = image.shape[0]+100

######################################################################################
#Main Loop
Start = True
while Start:

    #Get Events
    for events in pygame.event.get():
        if events.type == pygame.QUIT:
            Start = False
            pygame.quit()
    
    #Apply Logic
    success, image = video.read()
    hands, image = detector.findHands(image)

    if flag_for_exit_previous_window == 0:
            flag_for_exit_previous_window = 1
            cv.imshow("Image",image)
            cv.destroyWindow("Image")

    imgRGB = cv.cvtColor(image, cv.COLOR_BGR2RGB)
    imgRGB = np.rot90(imgRGB)                           #Rotating the Image Horizontally
    frame = pygame.surfarray.make_surface(imgRGB).convert()         #Connecting Opencv video and pygame window
    window.blit(frame, (0,0))

    BalloonRect.y -= Speed
    if (BalloonRect.y < 0):     #Checking for Reappearing balloon from the bottom again
        ResetBalloon()
        Speed+=1

    BalloonRect_2.y -= Speed_2
    if CountBlueBalloon%2 == 0:
        BalloonRect_2.x -= Speed_2
    else:
        BalloonRect_2.x += Speed_2
    if (BalloonRect_2.y < 0 or BalloonRect_2.x > 1200 or BalloonRect_2.x < 0):
        ResetBalloon_2()
        CountBlueBalloon +=1    
        Speed_2+=1
    
    BalloonRect_3.y -= Speed_3
    if (BalloonRect_3.y < 0):
        ResetBalloon_3()
        Speed_3+=1

    if hands:                      #Checking for the Hands
        hand = hands[0]
        x, y, temp = hand['lmList'][8]
        x = 1280 - x
 
        if BalloonRect.collidepoint(x, y):      #If Collide then Restart the Balloon, Increase Speed and Score
            ResetBalloon()
            window.blit(ImgPop,(x-75,y-25))     #Displaying the Popped Imaged as balloon is bursted
            Score += 1
            Speed += 1

        if BalloonRect_2.collidepoint(x, y):      #If Collide then Restart the Balloon, Increase Speed and Score
            ResetBalloon_2()
            window.blit(ImgPop,(x-75,y-25))     #Displaying the Popped Imaged as balloon is bursted
            Score += 1
            Speed_2 += 1

        if BalloonRect_3.collidepoint(x, y):      #If Collide then Restart the Balloon, Increase Speed and Score
            ResetBalloon_3()
            window.blit(ImgPop,(x-75,y-25))     #Displaying the Popped Imaged as balloon is bursted
            Score += 5
            Speed_3 += 1

    window.blit(ImgBalloon,BalloonRect)         #Displaying Balloon at BalloonRect position Created
    window.blit(ImgBalloon_2,BalloonRect_2)
    window.blit(ImgBalloon_3,BalloonRect_3)

    Time = int(TotalTime-(time.time() - StartTime))

    if (Time < 0):          #If Time Over then
        font = pygame.font.Font('E:/Extra Codes/Python/Python Projects/Virtual FunHub (Games)/Ballon Pop (Pygame)/Images_Project/Marcellus-Regular.ttf',50)
        textScore = font.render(f'Your Score :- {Score}',True,(255, 0, 0))
        textTime = font.render(f'Time UP',True,(255, 0, 0))
        window.blit(textScore,(450, 350))
        window.blit(textTime,(530, 275))
        ######################################################################################
        #Going Back to InterFace
        font_goback = pygame.font.Font('E:/Extra Codes/Python/Python Projects/Virtual FunHub (Games)/Ballon Pop (Pygame)/Images_Project/Marcellus-Regular.ttf',50)
        pygame.draw.rect(window, (255, 0, 0), pygame.Rect(0, 0, 80, 80))
        window.blit(font_goback.render("X", True, (255, 255, 255)), (20, 10))
        BalloonRect.y, BalloonRect_2.y, BalloonRect_3.y = 0, 0, 0
        if hands:
            hand1 = hands[0]
            lmlist = hand1["lmList"]
            x1, y1 = lmlist[8][:2]
            fingers = detector.fingersUp(hand1)
            if fingers[1] and fingers[2]:
                if 1270>=x1>=1200 and 0<=y1<=150:
                    pygame.display.quit()
                    image[:] = (0, 0, 0)
                    cv.putText(image, 'Loading...', (300, 400), cv.FONT_HERSHEY_SIMPLEX, 5, (0, 0, 255), 5)
                    cv.imshow("Image",image)
                    cv.waitKey(1)
                    print("Loading....")
                    exec(open("E:/Extra Codes/Python/Python Projects/Virtual FunHub (Games)/InterFace/main.py").read())
                    
    else:                   #Else Continue
        font = pygame.font.Font('E:/Extra Codes/Python/Python Projects/Virtual FunHub (Games)/Ballon Pop (Pygame)/Images_Project/Marcellus-Regular.ttf',50)
        textScore = font.render(f'Score :- {Score}',True,(255, 0, 0))
        textTime = font.render(f'Time :- {Time}',True,(255, 0, 0))
        window.blit(textScore,(35, 10))
        window.blit(textTime,(1050, 10))

    #Update Display
    pygame.display.update()

    #set FPS
    clock.tick(fps)
######################################################################################
