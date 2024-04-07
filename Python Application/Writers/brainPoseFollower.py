import numpy as np
import cv2 as cv
from Writers.instructionWriter import InstructionWriter

class BrainPoseFollower(InstructionWriter):
    
    brainPosHomogenous = np.array([[0.0, 7.0, -12.0, 1.0]]).reshape((4, 1))

    def __init__(self, inInstructionHandleValueSeparator, modeMask):
        super().__init__(inInstructionHandleValueSeparator, modeMask)
        
    def generateInstruction(self, detector, trackObjs, camCalib):
        instruction = "Brain" + self.inInstructionHandleValueSeparator 
  
        if len(trackObjs) > 0:
            face = trackObjs[0]

            rMat, jac = cv.Rodrigues(face["rVec"])
            angles, mtxR, mtxQ, Qx, Qy, Qz = cv.RQDecomp3x3(rMat)

            transfMat = np.zeros((4, 4))
            transfMat[0:3, 0:3] = rMat[:, :]
            transfMat[0:3, 3] = face["tVec"].reshape(3)[:]
            transfMat[3, 3] = 1

            brainWorldPos = transfMat @ BrainPoseFollower.brainPosHomogenous
            brainWorldPos = brainWorldPos.ravel()
            
            rotX = angles[2]
            rotY = (angles[1] + 90) % 360
            rotZ = (-angles[0] + 180) % 360
            
            instruction += str(round(brainWorldPos[0], 2)) + ";" + str(round(-brainWorldPos[1], 2)) + ";" + str(round(brainWorldPos[2], 2)) + ";" + str(round(rotX, 2)) + ";" + str(round(rotY, 2)) + ";" + str(round(rotZ, 2))

        else:
            instruction = ""

        return instruction
