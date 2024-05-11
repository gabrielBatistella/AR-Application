import numpy as np
import cv2 as cv
import math

from Connection.handler import Handler
from Modules.handTrackingModule import HandDetector
from Camera.cameraCalibration import CalibrationInfo

class HandlerAPNP(Handler):

    def __init__(self):
        super().__init__()
        self.calib = CalibrationInfo("Camera/calib_results/calculatedValues.npz")
        self.handDetector = HandDetector(maxHands=1, minDetectionCon=0.8, minTrackCon=0.5)
        
    def __del__(self):
        super().__del__()
        cv.destroyAllWindows()
        
    def operateOnData(self, data):
        frame_encoded = np.frombuffer(data, dtype=np.uint8)
        frame = cv.imdecode(frame_encoded, cv.IMREAD_COLOR)
        inv = cv.flip(frame, 1)
        img = inv.copy()
    
        hands, img = self.handDetector.findHands(frame, draw=True, flipType=True)
        
        if len(hands) > 0:
            hand = hands[0]
            lmList = hand["lmList"]
            
            palmPoints = []
            for index in self.handDetector.palmIds:
                palmPoints.append(np.array(lmList[index][0:2]))
            palmPoints = np.array(palmPoints, dtype=np.float32)
            
            palm3dPoints = None
            if hand["type"] == "Right":
                palm3dPoints = self.handDetector.rightPalm3dPoints
            else:
                palm3dPoints = self.handDetector.leftPalm3dPoints
            
            ret, rVec, tVec = cv.solvePnP(palm3dPoints, palmPoints, self.calib.camMatrix, self.calib.distCof, cv.SOLVEPNP_IPPE)
            tVec = np.reshape(tVec, 3)

            dist = round(math.hypot(tVec[0], tVec[1], tVec[2]), 2)
            print(dist, " cm")
        
        cv.imshow('img', img)
        key = cv.waitKey(1)

        return ""