from Writers.instructionWriter import InstructionWriter
import math
import os

def loadFile(filePath):
    with open(filePath, "rb") as file:
        data = file.read().hex()
    return data

class ObjectSpawner(InstructionWriter):
    
    def __init__(self, inInstructionHandleValueSeparator, modeMask):
        super().__init__(inInstructionHandleValueSeparator, modeMask)

        self.spawn = False
        self.following = False
        self.path = "C:/Users/Gabriel/Desktop/test/"

    def getDisableInstruction(self):
        instruction = "Spawn" + self.inInstructionHandleValueSeparator
        instruction += "Lost Track"
        return instruction

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
                
                x2 = (lmList[8][0] - camCalib.w/2)*hand["px2cmRate"][0]
                y2 = (-lmList[8][1] + camCalib.h/2)*hand["px2cmRate"][1]
                z2 = lmList[8][2]*hand["px2cmRate"][2] + hand["tVec"][2]
                
                dist = math.hypot(x2 - x1, y2 - y1, z2 - z1)
                
                xAvg = (x1+x2)/2
                yAvg = (y1+y2)/2
                zAvg = (z1+z2)/2
                
                #If thumb and index fingers are close
                if dist < 5:
                    if not self.spawn:
                        self.spawn = True
                    instruction += str(xAvg) + ";" + str(yAvg) + ";" + str(zAvg)
                
                else:
                    if self.spawn:
                        files = os.listdir(self.path)
                        fileName = files[0].split("-", 1)[0]
                        filePath = self.path + files[0]
                        fileHexData = loadFile(filePath)
                        instruction += "Spawn:" + str(xAvg) + ";" + str(yAvg) + ";" + str(zAvg) + "/" + fileName + "/" + fileHexData
                        self.spawn = False
                    else:
                        instruction = ""

                self.following = True
            
            else:
                if self.following:
                    instruction += "Lost Track"
                    self.spawn = False
                    self.following = False
                else:
                    instruction = ""

        else:
            if self.following:
                instruction += "Lost Track"
                self.spawn = False
                self.following = False
            else:
                instruction = ""
                    
        return instruction