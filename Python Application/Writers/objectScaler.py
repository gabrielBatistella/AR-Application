from Writers.instructionWriter import InstructionWriter
import math

class ObjectScaler(InstructionWriter):
    
    def __init__(self, inInstructionHandleValueSeparator, modeMask):
        super().__init__(inInstructionHandleValueSeparator, modeMask)

        self.holding = False
        self.xAvgInit = 0
        self.prevFilteredPoint = {4: None, 8: None}

    def generateInstruction(self, detector, trackObjs, camCalib):
        instruction = "Scale" + self.inInstructionHandleValueSeparator

        if len(trackObjs) > 0:
            hand = trackObjs[0]

            #Scale
            if hand["fingersUp"] == [1, 1, 1, 1, 1]:
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
                
                xAvg = (self.filteredPoint[4][0] + self.filteredPoint[8][0])/2
                yAvg = (self.filteredPoint[4][1] + self.filteredPoint[8][1])/2
                zAvg = (self.filteredPoint[4][2] + self.filteredPoint[8][2])/2
                
                if dist < 4:
                    if not self.holding:
                        self.holding = True
                        self.xAvgInit = xAvg
                        instruction += "Grab:" + str(round(xAvg, 2)) + ";" + str(round(yAvg, 2)) + ";" + str(round(zAvg, 2))

                    else:
                        scale = abs((self.xAvgInit - xAvg)/3, 3)
                        instruction += "Holding:" + str(round(scale,2))

                else:
                    if self.holding:
                        instruction += "Release:"
                        self.holding = False
                    instruction += str(round(xAvg, 2)) + ";" + str(round(yAvg, 2)) + ";" + str(round(zAvg, 2))      
                
            else:
                instruction = ""
                self.prevFilteredPoint = {4: None, 8: None}

        else:
            instruction = ""
            self.prevFilteredPoint = {4: None, 8: None}
                
        return instruction
