from Writers.instructionWriter import InstructionWriter
import math
import os

def loadFile(filePath):
    with open(filePath, "rb") as file:
        data = file.read().hex()
    return data

class ElectrodeSpawner(InstructionWriter):
    
    def __init__(self, inInstructionHandleValueSeparator, modeMask):
        super().__init__(inInstructionHandleValueSeparator, modeMask)

        self.spawn = False
        self.filter = False
        self.beta = 0.75
        self.Q1 = [0, 0, 0]
        self.Q2 = [0, 0, 0]
        self.Q3 = [0, 0, 0]

    def generateInstruction(self, detector, trackObjs, camCalib):
        instruction = "Spawn" + self.inInstructionHandleValueSeparator

        if len(trackObjs) > 0:
            hand = trackObjs[0]

            #If only index and middle fingers are up
            if hand["fingersUp"] == [1, 1, 0, 0, 0]:
                lmList = hand["lmList"]

                x1 = (lmList[4][0] - camCalib.w/2)*hand["px2cmRate"][0]
                y1 = (-lmList[4][1] + camCalib.h/2)*hand["px2cmRate"][1]
                z1 = lmList[4][2]*hand["px2cmRate"][2] + hand["tVec"][2]
                P1 = [x1, y1, z1]
                R1 = P1 [:]
                
                x2 = (lmList[5][0] - camCalib.w/2)*hand["px2cmRate"][0]
                y2 = (-lmList[5][1] + camCalib.h/2)*hand["px2cmRate"][1]
                z2 = lmList[5][2]*hand["px2cmRate"][2] + hand["tVec"][2]
                P2 = [x2, y2, z2]
                R2 = P2[:]
                
                x3 = (lmList[8][0] - camCalib.w/2)*hand["px2cmRate"][0]
                y3 = (-lmList[8][1] + camCalib.h/2)*hand["px2cmRate"][1]
                z3 = lmList[8][2]*hand["px2cmRate"][2] + hand["tVec"][2]
                P3 = [x3, y3, z3]
                R3 = P3[:]
                
                if not self.filter:
                    self.Q1 = P1[:]
                    self.Q2 = P2[:]
                    self.Q3 = P3[:]
                    self.filter = True
                
                for P, self.Q, R in ((P1, self.Q1, R1), (P2, self.Q1, R1), (P3, self.Q3, R3)):
                    for i in range(len(P)):
                        R[i] = P[i]*self.beta + self.Q[i]*(1-self.beta)
                        self.Q[i] = R[i]
                
                dist = math.hypot(R2[0] - R1[0], R2[1] - R2[1], R2[2] - R1[2])

                #If thumb and index fingers are close
                if dist < 5:
                    if not self.spawn:
                        self.spawn = True
                    instruction += str(x2) + ";" + str(y2) + ";" + str(z2) + "/" + str(x3) + ";" + str(y3) + ";" + str(z3)

                else:
                    if self.spawn:
                        instruction += "Spawn:" + str(x2) + ";" + str(y2) + ";" + str(z2) + "/" + str(x3) + ";" + str(y3) + ";" + str(z3)
                        self.spawn = False
                    else:
                        instruction = ""

            else:
                instruction = ""
                self.spawn = False

        else:
            instruction = ""
            self.spawn = False

        return instruction