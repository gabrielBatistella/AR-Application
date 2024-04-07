from Writers.instructionWriter import InstructionWriter
import math

class ObjectRotator(InstructionWriter):
    
    def __init__(self, inInstructionHandleValueSeparator, modeMask):
        super().__init__(inInstructionHandleValueSeparator, modeMask)

        self.holding = False
        self.xAvgInit = 0
        self.yAvgInit = 0
        self.zAvgInit = 0
        self.filteredPoint = {4: None, 8: None}

    def generateInstruction(self, detector, trackObjs, camCalib):
        instruction = "Rotate" + self.inInstructionHandleValueSeparator

        if len(trackObjs) > 0:
            hand = trackObjs[0]

            #Rotate
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
            
                #If thumb is touching index finger second landmark
                if dist < 4:
                    if not self.holding:
                        self.xAvgInit = xAvg
                        self.yAvgInit = yAvg
                        self.zAvgInit = zAvg
                        self.holding = True
                        instruction += "Grab:" + str(round(xAvg, 2)) + ";" + str(round(yAvg, 2)) + ";" + str(round(zAvg, 2))
                    else:
                        rollDelta = (self.xAvgInit - xAvg)/10*360
                        pitchDelta = (self.yAvgInit - yAvg)/10*360
                        yawDelta = (self.zAvgInit - zAvg)/10*360
                        instruction += "Holding:" + str(round(rollDelta, 2)) + ";" + str(round(pitchDelta, 2)) + ";" + str(round(yawDelta, 2))

                else:
                    if self.holding:
                        instruction += "Release:"
                        self.holding = False
                    instruction += str(round(xAvg, 2)) + ";" + str(round(yAvg, 2)) + ";" + str(round(zAvg, 2))

            else:
                instruction = ""
                self.filteredPoint = {4: None, 8: None}
            
        else:
            instruction = ""
            self.filteredPoint = {4: None, 8: None}

        return instruction