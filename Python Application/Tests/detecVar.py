import numpy as np
import cv2 as cv

from Connection.handler import Handler
from Modules.handTrackingModule import HandDetector

class DetecVar(Handler):

    def __init__(self):
        super().__init__()
        self.detectionCon = 0.8
        self.trackCon = 0.5

        self.handDetector = HandDetector(maxHands=1, minDetectionCon=self.detectionCon, minTrackCon=self.trackCon)

    def __del__(self):
        super().__del__()
        cv.destroyAllWindows()

        

    def operateOnData(self, data):
        frame_encoded = np.frombuffer(data, dtype=np.uint8)
        frame = cv.imdecode(frame_encoded, cv.IMREAD_COLOR)
        inv = cv.flip(frame, 1)
        img = inv.copy()
    
        hands, img = self.handDetector.findHands(frame, draw=True, flipType=True)
        
        cv.imshow('img', img)
        
        key = cv.waitKey(1)
        if key == ord('d'):
            self.detectionCon = float(input("Insert New Detection Confidence: "))
            self.handDetector = HandDetector(maxHands=1, minDetectionCon=self.detectionCon, minTrackCon=self.trackCon)

        elif key == ord('t'):
            self.trackCon = float(input("Insert New Track Confidence: "))
            self.handDetector = HandDetector(maxHands=1, minDetectionCon=self.detectionCon, minTrackCon=self.trackCon)

        return ""