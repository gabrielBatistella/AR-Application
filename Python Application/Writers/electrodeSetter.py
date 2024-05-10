from Writers.instructionWriter import InstructionWriter
import math

def loadFile(filePath):
    with open(filePath, "rb") as file:
        data = file.read().hex()
    return data

class ElectrodeSetter(InstructionWriter):
    
    def __init__(self, inInstructionHandleValueSeparator, modeMask):
        super().__init__(inInstructionHandleValueSeparator, modeMask)

        self.spawn = False
        
        self.filteredPoints = {}

    def generateInstruction(self, detector, trackObjs, camCalib):
        instruction = "Electrode" + self.inInstructionHandleValueSeparator

        if len(trackObjs) > 0:
            hand = trackObjs[0]

            #If only index and middle fingers are up
            if hand["fingersUp"] == [1, 1, 0, 0, 0] or hand["fingersUp"] == [0, 1, 0, 0, 0]:
                lmList = hand["lmList"]

                for id in (4, 5, 8):
                    x = (lmList[id][0] - camCalib.w/2)*hand["px2cmRate"][0]
                    y = (-lmList[id][1] + camCalib.h/2)*hand["px2cmRate"][1]
                    z = lmList[id][2]*hand["px2cmRate"][2] + hand["tVec"][2]
                    
                    if id not in self.filteredPoints:
                        self.filteredPoints[id] = (x, y, z)
                    
                    self.filteredPoints[id] = InstructionWriter.filterPointEWA((x, y, z), self.filteredPoints[id])
                
                dist = math.hypot(self.filteredPoints[4][0] - self.filteredPoints[5][0], self.filteredPoints[4][1] - self.filteredPoints[5][1], self.filteredPoints[4][2] - self.filteredPoints[5][2])

                if dist < 2:
                    if not self.spawn:
                        self.spawn = True
                        instruction += "Set:"
                    instruction += str(round(self.filteredPoints[8][0], 2)) + ";" + str(round(self.filteredPoints[8][1], 2)) + ";" + str(round(self.filteredPoints[8][2], 2)) + "/" + str(round(self.filteredPoints[5][0], 2)) + ";" + str(round(self.filteredPoints[5][1], 2)) + ";" + str(round(self.filteredPoints[5][2], 2))

                else:
                    if self.spawn:
                        self.spawn = False
                    instruction += str(round(self.filteredPoints[8][0], 2)) + ";" + str(round(self.filteredPoints[8][1], 2)) + ";" + str(round(self.filteredPoints[8][2], 2)) + "/" + str(round(self.filteredPoints[5][0], 2)) + ";" + str(round(self.filteredPoints[5][1], 2)) + ";" + str(round(self.filteredPoints[5][2], 2))
                    
            else:
                instruction = ""
                self.spawn = False
                self.filteredPoints = {}

        else:
            instruction = ""
            self.spawn = False
            self.filteredPoints = {}

        return instruction