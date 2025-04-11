import cv2
import cvzone
import numpy as np
from cvzone.HandTrackingModule import HandDetector

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

detector = HandDetector(detectionCon=0.8)
# colorR = 0, 266, 0

cx, cy = 100, 100
w, h = 200, 200

class DrawRec():
    def __init__(self, posCenter, size=[200,200]):
        self.posCenter = posCenter
        self.size = size
        self.color= (255,0,0)

    def update(self, cursor):
        cx,cy = self.posCenter
        w,h = self.size

        if (cx - w // 2 < cursor[0] < cx + w // 2 and
                cy - h // 2 < cursor[1] < cy + h // 2):
           self.posCenter = cursor[0], cursor[1]

rectlist = []
for x in range(5):
  rectlist.append(DrawRec([x*250+150,150]))


while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    hands, img = detector.findHands(img)

    if hands:
        lmList = hands[0]["lmList"]

        point1 = lmList[8][:2]
        point2 = lmList[12][:2]


        distance, info, img = detector.findDistance(point1, point2, img)
        print(distance)

        cursor = lmList[8]
        if distance < 37:
         for rect in rectlist:
           rect.update(cursor)



    imgnew = np.zeros_like(img, np.uint8)
    for rect in rectlist:
     cx, cy = rect.posCenter
     w,h = rect.size
     color= rect.color
     cv2.rectangle(imgnew, (cx - w // 2, cy - h // 2),
                  (cx + w // 2, cy + h // 2), color, cv2.FILLED)

    out = img.copy()
    alpha= 0.1
    mask = imgnew.astype(bool)
    out[mask]=cv2.addWeighted(img, alpha, imgnew, 1 - alpha, 0)[mask]

    cv2.imshow("Image", out)
    key = cv2.waitKey(1)
    if key == ord('q'):  # Press 'q' to quit
        break


