import cv2
from cvzone.HandTrackingModule import HandDetector
import cvzone
import numpy as np
import math

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)
detector = HandDetector(detectionCon=0.8)

colorR = (255, 0, 255)
cx, cy, w, h = 100, 100, 200, 200
menu = 0
temp = 0
opt = 0
optshow = None
wait = 0

while True:
    success, img = cap.read()
    hands, img = detector.findHands(img, draw=False)

    if hands and detector.fingersUp(hands[0]) == [0, 1, 1, 0, 0]:
        lmList = hands[0]['lmList']

        x1, y1, z1 = lmList[8]
        x2, y2, z2 = lmList[12]
        d = int(math.sqrt((y2 - y1) ** 2 + (x2 - x1) ** 2))
        #cvzone.putTextRect(img, "Loading Menu..." , (x1+50, y1-100), scale= 2, thickness= 1, colorT=(255, 255, 255), colorR=(150, 150, 150))
        #print (x1 , y1)
        if d < 40:
            ym = (y1+y2)/2
            if menu == 0:
                if wait == 0:   
                    yc = ym
                    wait = 1
                elif wait == 1:
                    dy = ym - yc
                    if dy > 70 and temp == 0:
                        temp = 1
                    if 0 < temp < 30:
                        cvzone.putTextRect(img, "Loading Menu..." , (x1+50, y1), scale= 2, thickness= 1, colorT=(255, 255, 255), colorR=(150, 150, 150))
                        temp += 1
                        if temp == 15:
                            menu = 1
                            #Writer menu = 1
                            display = 1
                            wait = 0
                            temp = 0

            if menu == 1:
                xm = (x1+x2)/2
                if wait == 0:
                    yc = ym
                    xc = xm
                    wait = 1

                elif wait == 1:
                    dy = ym - yc
                    dx = xm - xc
                    porc = abs(round(100*dy/70))
                    print (porc,"%")
                    if dx < -20:
                        xc = xm
                    elif dx > 60:
                        optshow = opt
                        menu = 0
                        #Writer menu = opt
                    elif dy > 70:
                        opt += 1
                        wait = 0
                        if opt == 2:
                            opt = -1
                    elif dy < -70:
                        opt -= 1
                        wait = 0
                        if opt == -2:
                            opt = 1
                    elif opt == 0:
                        cvzone.putTextRect(img, "Zoom" , (x1+50, y1-60), scale= 2, thickness= 1, colorT=(255, 255, 255), colorR=(150, 150, 150))
                        cvzone.putTextRect(img, "Move" , (x1+50, y1), scale= 3, thickness= 4, colorT=(255, 255, 255), colorR=(150, 150, 150))
                        cvzone.putTextRect(img, "Rotate" , (x1+50, y1+50), scale= 2, thickness= 1, colorT=(255, 255, 255), colorR=(150, 150, 150))
                    elif opt == -1:
                        cvzone.putTextRect(img, "Zoom" , (x1+50, y1), scale= 3, thickness= 4, colorT=(255, 255, 255), colorR=(150, 150, 150))
                        cvzone.putTextRect(img, "Move" , (x1+50, y1+50), scale= 2, thickness= 1, colorT=(255, 255, 255), colorR=(150, 150, 150))
                        cvzone.putTextRect(img, "Rotate" , (x1+50, y1-60), scale= 2, thickness= 1, colorT=(255, 255, 255), colorR=(150, 150, 150))
                    elif opt == 1:
                        cvzone.putTextRect(img, "Zoom" , (x1+50, y1-60), scale= 2, thickness= 1, colorT=(255, 255, 255), colorR=(150, 150, 150))
                        cvzone.putTextRect(img, "Move" , (x1+50, y1+50), scale= 2, thickness= 1, colorT=(255, 255, 255), colorR=(150, 150, 150))
                        cvzone.putTextRect(img, "Rotate" , (x1+50, y1), scale= 3, thickness= 4, colorT=(255, 255, 255), colorR=(150, 150, 150))
                    
        else:
            menu = 0
            wait = 0

    if optshow == 0:
        cvzone.putTextRect(img, "Move" , (50, 50), scale= 2, thickness= 2, colorT=(255, 255, 255), colorR=(150, 150, 150))
    elif optshow == -1:
        cvzone.putTextRect(img, "Zoom" , (50, 50), scale= 2, thickness= 2, colorT=(255, 255, 255), colorR=(150, 150, 150))
    elif optshow == 1:
        cvzone.putTextRect(img, "Rotate" , (50, 50), scale= 2, thickness= 2, colorT=(255, 255, 255), colorR=(150, 150, 150))



    cv2.imshow("Image", img)
    key = cv2.waitKey(1)
    if key == ord('q'):
        cap.release()
        cv2.destroyAllWindows()
        break