from Writers.instructionWriter import InstructionWriter
import math

class ObjectTranslator(InstructionWriter):
    
    def __init__(self, inInstructionHandleValueSeparator, modeMask):
        super().__init__(inInstructionHandleValueSeparator, modeMask)

        self.holding = False
        
        self.xAvgInit = 0
        self.yAvgInit = 0
        self.zAvgInit = 0
        
        self.filteredPoints = {}

    def generateInstruction(self, detector, trackObjs, camCalib):
        instruction = "Translate" + self.inInstructionHandleValueSeparator

        if len(trackObjs) > 0:
            hand = trackObjs[0]

            #Translate
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
                
                #If thumb and index finger are close
                if dist < 4:
                    
                    if not self.holding:
                        self.xAvgInit = xAvg
                        self.yAvgInit = yAvg
                        self.zAvgInit = zAvg
                        self.holding = True
                        instruction += "Grab:" + str(round(xAvg, 2)) + ";" + str(round(yAvg, 2)) + ";" + str(round(zAvg, 2))
                    else:
                        xDelta = xAvg - self.xAvgInit
                        yDelta = yAvg - self.yAvgInit
                        zDelta = zAvg - self.zAvgInit
                        instruction += "Holding:" + str(round(xDelta, 2)) + ";" + str(round(yDelta, 2)) + ";" + str(round(zDelta, 2))

                else:
                    if self.holding:
                        instruction += "Release:"
                        self.holding = False
                    instruction += str(round(xAvg, 2)) + ";" + str(round(yAvg, 2)) + ";" + str(round(zAvg, 2))

            else:
                instruction = ""
                self.filteredPoints = {}

        else:
            instruction = ""
            self.filteredPoints = {}

        return instruction