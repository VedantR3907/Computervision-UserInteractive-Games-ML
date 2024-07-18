from email.mime import image
from cvzone.HandTrackingModule import HandDetector
import cv2
import csv
import cvzone
import time

# for Webcam
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)
detector = HandDetector(detectionCon=0.8,maxHands=1)

timer = 0

# for setting mcqs
class MCQ():
    def __init__(self, data):
        self.question = data[0]
        self.choice1 = data[1]
        self.choice2 = data[2]
        self.choice3 = data[3]
        self.choice4 = data[4]
        self.answer = int(data[5])

        self.userAns = None

    def update(self, cursor, bboxs):
        for x, bbox in enumerate(bboxs):
            x1, y1, x2, y2 = bbox
            if x1 < cursor[0] < x2 and y1 < cursor[1] < y2:
                self.userAns = x + 1
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), cv2.FILLED)


# Import csv file data
pathCSV = "E:/Extra Codes/Python/Python Projects/Virtual FunHub (Games)/Virtual_Quiz/Quiz.csv"
with open(pathCSV, newline='\n') as f:
    reader = csv.reader(f)
    dataAll = list(reader)[1:]

# Create Object for each MCQ
mcqList = []
for q in dataAll:
    mcqList.append(MCQ(q))

print("Total MCQ Objects Created:", len(mcqList))

qNo = 0
qTotal = len(dataAll)
while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    hands, img = detector.findHands(img, flipType=False)
    if qNo < qTotal:
        mcq = mcqList[qNo]

        img, bbox = cvzone.putTextRect(img, mcq.question, [100, 100], 2, 2, offset=50, border=5)
        img, bbox1 = cvzone.putTextRect(img, mcq.choice1, [100, 250], 2, 2, offset=50, border=5)
        img, bbox2 = cvzone.putTextRect(img, mcq.choice2, [400, 250], 2, 2, offset=50, border=5)
        img, bbox3 = cvzone.putTextRect(img, mcq.choice3, [100, 400], 2, 2, offset=50, border=5)
        img, bbox4 = cvzone.putTextRect(img, mcq.choice4, [400, 400], 2, 2, offset=50, border=5)

        if hands:
            lmList = hands[0]['lmList']
            cursor = lmList[8]

            length, info = detector.findDistance(lmList[8][0:2], lmList[12][0:2])[0:2]
            print(length)
            if length < 40:
                timer +=1    #Counting Timer

                if timer>30:
                    mcq.update(cursor, [bbox1, bbox2, bbox3, bbox4])
                if mcq.userAns is not None:
                    time.sleep(0.3)
                    qNo += 1
                    timer = 0
    else:
        score = 0
        for mcq in mcqList:
            if mcq.answer == mcq.userAns:
                score += 1
        score = round((score / qTotal) * 100, 2)
        img, _ = cvzone.putTextRect(img, "Quiz Completed", [250, 300], 2, 2, offset=50, border=5)
        img, _ = cvzone.putTextRect(img, f'Your Score: {score}%', [700, 300], 2, 2, offset=50, border=5)

        # Draw Progress Bar
        barValue = 150 + (950 // qTotal) * qNo
        cv2.rectangle(img, (150, 600), (barValue, 650), (0, 255, 0), cv2.FILLED)
        cv2.rectangle(img, (150, 600), (1100, 650), (255, 0, 255), 5)
        img, _ = cvzone.putTextRect(img, f'{round((qNo / qTotal) * 100)}%', [1130, 635], 2, 2, offset=16)
        ######################################################################################
        #Going Back to interface Options
        cv2.rectangle(img, (0, 0), (90,90), (0, 0, 255), cv2.FILLED)
        cv2.putText(img, "X", (15,73),cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 255, 255), 5)
        hand, img = detector.findHands(img)
        if hand:
            hand1 = hand[0]
            lmlist = hand1["lmList"]
            x1, y1 = lmlist[8][:2]
            fingers = detector.fingersUp(hand1)
            if fingers[1] and fingers[2]:
                if 0<=x1<=110 and 0<=y1<=110:   
                    print("Loading....")
                    cv2.destroyWindow("Image")
                    img[:] = (0, 0, 0)
                    cv2.putText(img, 'Loading...', (300, 400), cv2.FONT_HERSHEY_SIMPLEX, 5, (0, 0, 255), 5)
                    cv2.imshow("Image",img)
                    cv2.waitKey(1)
                    exec(open("E:/Extra Codes/Python/Python Projects/Virtual FunHub (Games)/InterFace/main.py").read())
        ######################################################################################


    cv2.imshow("Img", img)
    cv2.waitKey(1)