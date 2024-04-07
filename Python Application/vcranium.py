import numpy as np
import cv2 as cv

from Camera.cameraCalibration import CalibrationInfo
from Modules.handTrackingModule import HandDetector
from Modules.faceMeshModule import FaceMeshDetector

from Connection.handler import Handler

from Writers.menuHandler import MenuHandler
from Writers.fingerTipsFollower import FingerTipsFollower
from Writers.objectSpawner import ObjectSpawner
from Writers.objectRemover import ObjectRemover
from Writers.objectTranslator import ObjectTranslator
from Writers.objectRotator import ObjectRotator
from Writers.objectScaler import ObjectScaler
from Writers.freeTransformer import FreeTransformer
from Writers.electrodeSetter import ElectrodeSetter
from Writers.brainPoseFollower import BrainPoseFollower

class VCranium(Handler):
    
    inBodyInstructionSeparator = "&"
    inInstructionHandleValueSeparator = "="

    def __init__(self):
        super().__init__()

        self.calib = CalibrationInfo("Camera/calib_results/calculatedValues.npz")

        self.handDetector = HandDetector(maxHands=2, minDetectionCon=0.8)
        self.handInstructionWriters = [
            MenuHandler(self.__class__.inInstructionHandleValueSeparator, 0b111111),
            FingerTipsFollower(self.__class__.inInstructionHandleValueSeparator, 0b100000),
            ObjectSpawner(self.__class__.inInstructionHandleValueSeparator, 0b010000),
            ObjectRemover(self.__class__.inInstructionHandleValueSeparator, 0b010000),
            ObjectTranslator(self.__class__.inInstructionHandleValueSeparator, 0b001000),
            ObjectRotator(self.__class__.inInstructionHandleValueSeparator, 0b001000),
            ObjectScaler(self.__class__.inInstructionHandleValueSeparator, 0b001000),
            FreeTransformer(self.__class__.inInstructionHandleValueSeparator, 0b000100),
            ElectrodeSetter(self.__class__.inInstructionHandleValueSeparator, 0b000010)
        ]

        self.faceDetector = FaceMeshDetector(maxFaces=1, minDetectionCon=0.5)
        self.faceInstructionWriters = [
            BrainPoseFollower(self.__class__.inInstructionHandleValueSeparator, 0b000001)
        ]

    def __del__(self):
        super().__del__()

    def operateOnData(self, data):
        frame_encoded = np.frombuffer(data, dtype=np.uint8)
        frame = cv.imdecode(frame_encoded, cv.IMREAD_COLOR)

        initialMode = self.handInstructionWriters[0].modeCurrent

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
                if writer.shouldExecuteInMode(initialMode):
                    instruction = writer.generateInstruction(self.handDetector, hands, self.calib)

                    if instruction != "":
                        result += instruction + self.__class__.inBodyInstructionSeparator

        if len(self.faceInstructionWriters) > 0:
            faces = self.faceDetector.findFaceMesh(frame, draw=False)

            for face in faces:
                featureMarkPoints = []
                for index in self.faceDetector.featureMarkIds:
                    featureMarkPoints.append(np.array(face["lmList"][index][0:2]))
                featureMarkPoints = np.array(featureMarkPoints, dtype=np.float32)

                ret, rVec, tVec = cv.solvePnP(self.faceDetector.featureMark3dPoints, featureMarkPoints, self.calib.camMatrix, self.calib.distCof, cv.SOLVEPNP_IPPE)
                rVec = np.reshape(rVec, 3)
                tVec = np.reshape(tVec, 3)
                face["rVec"] = rVec[:]
                face["tVec"] = tVec[:]

            for writer in self.faceInstructionWriters:
                if writer.shouldExecuteInMode(initialMode):
                    instruction = writer.generateInstruction(self.faceDetector, faces, self.calib)

                    if instruction != "":
                        result += instruction + self.__class__.inBodyInstructionSeparator

        return result