import numpy as np
import cv2 as cv
from Writers.instructionWriter import InstructionWriter

class BrainPoseFollower(InstructionWriter):
    
    brainPosHomogenous = np.array([[0.0, 7.0, -12.0, 1.0]]).reshape((4, 1))

    def __init__(self, inInstructionHandleValueSeparator, modeMask):
        super().__init__(inInstructionHandleValueSeparator, modeMask)
        
        self.filteredPoints = {}
        
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
            
            if "pos" not in self.filteredPoints:
                self.filteredPoints["pos"] = brainWorldPos
                
            self.filteredPoints["pos"] = InstructionWriter.filterPointEWA(brainWorldPos, self.filteredPoints["pos"])
            
            rotX = -angles[2]
            rotY = (angles[1] - 90)
            rotZ = -(-angles[0] + 180)
            
            if "ang" not in self.filteredPoints:
                self.filteredPoints["ang"] = (rotX, rotY, rotZ)
                
            self.filteredPoints["ang"] = InstructionWriter.filterPointEWA((rotX, rotY, rotZ), self.filteredPoints["ang"])
            
            instruction += str(round(self.filteredPoints["pos"][0], 2)) + ";" + str(round(-self.filteredPoints["pos"][1], 2)) + ";" + str(round(self.filteredPoints["pos"][2], 2)) + ";" + str(round(self.filteredPoints["ang"][0], 2)) + ";" + str(round(self.filteredPoints["ang"][1], 2)) + ";" + str(round(self.filteredPoints["ang"][2], 2))

        else:
            instruction = ""
            self.filteredPoints = {}

        return instruction
