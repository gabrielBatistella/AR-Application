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
        self.filteredPoint = {4: None, 5: None, 8: None}

    def generateInstruction(self, detector, trackObjs, camCalib):
        instruction = "Electrode" + self.inInstructionHandleValueSeparator

        if len(trackObjs) > 0:
            hand = trackObjs[0]

            #If only index and middle fingers are up
            if hand["fingersUp"] == [1, 1, 0, 0, 0]:
                lmList = hand["lmList"]

                for id in (4, 8):
                    x = (lmList[id][0] - camCalib.w/2)*hand["px2cmRate"][0]
                    y = (-lmList[id][1] + camCalib.h/2)*hand["px2cmRate"][1]
                    z = lmList[id][2]*hand["px2cmRate"][2] + hand["tVec"][2]
                    
                    if self.filteredPoint[id] == None:
                        self.filteredPoint[id] = (x, y, z)
                    
                    InstructionWriter.filterPointEWA((x, y, z), self.filteredPoint[id])
                    
                    self.filteredPoint[id] = (x, y, z)
                
                dist = math.hypot(self.filteredPoint[4][0] - self.filteredPoint[8][0], self.filteredPoint[4][1] - self.filteredPoint[8][1], self.filteredPoint[4][2] - self.filteredPoint[8][2])

                if dist < 5:
                    if not self.spawn:
                        self.spawn = True
                    instruction += str(round(self.filteredPoint[8][0], 2)) + ";" + str(round(self.filteredPoint[8][1], 2)) + ";" + str(round(self.filteredPoint[8][2], 2)) + "/" + str(round(self.filteredPoint[5][0], 2)) + ";" + str(round(self.filteredPoint[5][1], 2)) + ";" + str(round(self.filteredPoint[5][2], 2))

                else:
                    if self.spawn:
                        instruction += "Set:" + str(round(self.filteredPoint[8][0], 2)) + ";" + str(round(self.filteredPoint[8][1], 2)) + ";" + str(round(self.filteredPoint[8][2], 2)) + "/" + str(round(self.filteredPoint[5][0], 2)) + ";" + str(round(self.filteredPoint[5][1], 2)) + ";" + str(round(self.filteredPoint[5][2], 2))
                        self.spawn = False
                    else:
                        instruction = ""

            else:
                instruction = ""
                self.spawn = False
                self.filteredPoint = {4: None, 5: None, 8: None}

        else:
            instruction = ""
            self.spawn = False
            self.filteredPoint = {4: None, 5: None, 8: None}

        return instruction