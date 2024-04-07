from Writers.instructionWriter import InstructionWriter
import math
import os

def loadFile(filePath):
    with open(filePath, "rb") as file:
        data = file.read().hex()
    return data

def getFileInfo(folderPath):
    files = os.listdir(folderPath)
    filePath = folderPath + files[0]
    fileHexData = loadFile(filePath)
    fileName = files[0].split("-", 1)[0]
    return fileHexData, fileName

class ObjectSpawner(InstructionWriter):
    
    path = "C:/Users/Gabriel/Desktop/test/"
    
    def __init__(self, inInstructionHandleValueSeparator, modeMask):
        super().__init__(inInstructionHandleValueSeparator, modeMask)

        self.spawn = False
        
        self.filteredPoints = {}

    def generateInstruction(self, detector, trackObjs, camCalib):
        instruction = "Spawn" + self.inInstructionHandleValueSeparator

        if len(trackObjs) > 0:
            hand = trackObjs[0]

            #If only index and middle fingers are up
            if hand["fingersUp"] == [1, 1, 0, 0, 0]:
                lmList = hand["lmList"]
                
                for id in (4, 8):
                    x = (lmList[id][0] - camCalib.w/2)*hand["px2cmRate"][0]
                    y = (-lmList[id][1] + camCalib.h/2)*hand["px2cmRate"][1]
                    z = lmList[id][2]*hand["px2cmRate"][2] + hand["tVec"][2]
                    
                    if id not in self.filteredPoints:
                        self.filteredPoints[id] = (x, y, z)
                    
                    self.filteredPoints[id] = InstructionWriter.filterPointEWA((x, y, z), self.filteredPoints[id])
                
                dist = math.hypot(self.filteredPoints[4][0] - self.filteredPoints[8][0], self.filteredPoints[4][1] - self.filteredPoints[8][1], self.filteredPoints[4][2] - self.filteredPoints[8][2])
                
                xAvg = (self.filteredPoints[4][0] + self.filteredPoints[8][0])/2
                yAvg = (self.filteredPoints[4][1] + self.filteredPoints[8][1])/2
                zAvg = (self.filteredPoints[4][2] + self.filteredPoints[8][2])/2
                
                #If thumb and index fingers are close
                if dist < 5:
                    if not self.spawn:
                        self.spawn = True
                    instruction += str(round(xAvg, 2)) + ";" + str(round(yAvg, 2)) + ";" + str(round(zAvg, 2))
                
                else:
                    if self.spawn:
                        fileHexData, fileName = getFileInfo(ObjectSpawner.path)
                        instruction += "Spawn:" + str(round(xAvg, 2)) + ";" + str(round(yAvg, 2)) + ";" + str(round(zAvg, 2)) + "/" + fileName + "/" + fileHexData
                        self.spawn = False
                    else:
                        instruction = ""
            
            else:
                instruction = ""
                self.spawn = False
                self.filteredPoints = {}

        else:
            instruction = ""
            self.spawn = False
            self.filteredPoints = {}
                    
        return instruction