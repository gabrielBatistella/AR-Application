import numpy as np
import cv2 as cv

from Connection.handler import Handler
from Modules.handTrackingModule import HandDetector
from Camera.cameraCalibration import CalibrationInfo

class HandlerB(Handler):

    def __init__(self):
        super().__init__()
        self.calib = CalibrationInfo("Camera/calib_results/calculatedValues.npz")
        self.handDetector = HandDetector(maxHands=1, minDetectionCon=0.8, minTrackCon=0.5)
        
        self.betas = [1 - 1/i for i in range(1, 10+1)]
        self.filteredPoints = {beta: None for beta in self.betas}
        self.pointsHistory = {beta: [] for beta in self.betas}

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
            rVec = np.reshape(rVec, 3)
            tVec = np.reshape(tVec, 3)
            
            px2cmRate_x = tVec[0]/(lmList[0][0] - self.calib.w/2)
            px2cmRate_y = -tVec[1]/(-lmList[0][1] + self.calib.h/2)
            px2cmRate_z = px2cmRate_x
            
            x = (lmList[8][0] - self.calib.w/2)*px2cmRate_x
            y = (-lmList[8][1] + self.calib.h/2)*px2cmRate_y
            z = lmList[8][2]*px2cmRate_z + tVec[2]
            
            for beta in self.betas:
                if self.filteredPoints[beta] is None:
                    self.filteredPoints[beta] = (x, y, z)

                previousFilteredPoint = self.filteredPoints[beta]
                realPoint = (x, y, z)

                self.filteredPoints[beta] = [previousFilteredPoint[i]*beta + realPoint[i]*(1-beta) for i in range(3)]
                self.pointsHistory[beta].append(self.filteredPoints[beta])
        
        else:
            self.filteredPoints = {beta: None for beta in self.betas}
        
        cv.imshow('img', img)

        key = cv.waitKey(1)
        if key == ord(' '):
            for beta in self.betas:
                with open(f"Tests/test_results/latency/latency_beta{round(beta, 3)}.txt", "w") as f:
                    for point in self.pointsHistory[beta]:
                        f.write(f"{point[0]}, {point[1]}, {point[2]}\n")

        return ""