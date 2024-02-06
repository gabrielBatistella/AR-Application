import socket
import numpy as np
import cv2 as cv

from Connection.tcpServer import TCPServer
from Camera.cameraCalibration import CalibrationInfo
from Modules.handTrackingModule import HandDetector
from Modules.faceMeshModule import FaceMeshDetector
from Writers.followIndexFinger import FollowIndexFinger

class VCraniumServer(TCPServer):
    
    headerBodySeparator = "?"
    inHeaderInfoSeparator = "|"
    inBodyInstructionSeparator = "&"
    inInstructionHandleValueSeparator = "="

    def __init__(self, ip, port):
        super().__init__(ip, port)

        self.calib = CalibrationInfo("Camera/calib_results/calculatedValues.npz")

        self.handDetector = HandDetector(maxHands=2, minDetectionCon=0.8)
        self.handInstructionWriters = [
            FollowIndexFinger(self.__class__.inInstructionHandleValueSeparator)
        ]

        #self.faceDetector = FaceMeshDetector(maxFaces=1, minDetectionCon=0.5)
        #self.faceInstructionWriters = []

    def _operateOnDataReceived(self, data):
        frame_encoded = np.frombuffer(data, dtype=np.uint8)
        frame = cv.imdecode(frame_encoded, cv.IMREAD_COLOR)

        result = ""

        if len(self.handInstructionWriters) > 0:
            hands = self.handDetector.findHands(frame, draw=False, flipType=False)

            for hand in hands:
                palmPoints = []
                for index in self.handDetector.palmIds:
                    palmPoints.append(np.array(hand["lmList"][index][0:2]))
                palmPoints = np.array(palmPoints, dtype=np.float32)
                
                palm3dPoints = None
                if hand["type"] == "Right":
                    palm3dPoints = self.handDetector.rightPalm3dPoints
                else:
                    palm3dPoints = self.handDetector.leftPalm3dPoints

                ret, rVec, tVec = cv.solvePnP(palm3dPoints, palmPoints, self.calib.camMatrix, self.calib.distCof, cv.SOLVEPNP_IPPE)
                rVec = np.reshape(rVec, 3)
                tVec = np.reshape(tVec, 3)
                hand["rVec"] = rVec[:]
                hand["tVec"] = tVec[:]

                px2cmRate_x = tVec[0]/(hand["lmList"][0][0] - self.calib.w/2)
                px2cmRate_y = -tVec[1]/(-hand["lmList"][0][1] + self.calib.h/2)
                px2cmRate_z = px2cmRate_x
                hand["px2cmRate"] = [px2cmRate_x, px2cmRate_y, px2cmRate_z]

                hand["fingersUp"] = self.handDetector.fingersUp(hand)

            for writer in self.handInstructionWriters:
                instruction = writer.generateInstruction(self.handDetector, hands, self.calib)
                if instruction != "":
                    result += instruction + self.inBodyInstructionSeparator

        return result
        

        
def main():
    HOSTNAME = socket.gethostname()
    HOST = socket.gethostbyname(HOSTNAME)

    server = VCraniumServer(HOST, 5050)
    server.run()

if __name__ == '__main__' : main()