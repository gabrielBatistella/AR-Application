from Writers.instructionWriter import InstructionWriter
import math

class ObjectRemover(InstructionWriter):
    
    def __init__(self, inInstructionHandleValueSeparator, modeMask):
        super().__init__(inInstructionHandleValueSeparator, modeMask)

        self.delete = False
        self.prevFilteredPoint = {4: None, 5: None, 8: None, 12: None}

    def generateInstruction(self, detector, trackObjs, camCalib):
        instruction = "Remove" + self.inInstructionHandleValueSeparator

        if len(trackObjs) > 0:
            hand = trackObjs[0]

            #Rotate
            if hand["fingersUp"] == [1, 1, 1, 0, 0]:
                lmList = hand["lmList"]
                
                for id in (4, 5, 8, 12):
                    x = (lmList[id][0] - camCalib.w/2)*hand["px2cmRate"][0]
                    y = (-lmList[id][1] + camCalib.h/2)*hand["px2cmRate"][1]
                    z = lmList[id][2]*hand["px2cmRate"][2] + hand["tVec"][2]
                    
                    if self.filteredPoint[id] == None:
                        self.filteredPoint[id] = (x, y, z)
                    
                    InstructionWriter.filterPointEWA((x, y, z), self.filteredPoint[id])
                    
                    self.filteredPoint[id] = (x, y, z)
                
                dist = math.hypot(self.filteredPoint[4][0] - self.filteredPoint[5][0], self.filteredPoint[4][1] - self.filteredPoint[5][1], self.filteredPoint[4][2] - self.filteredPoint[5][2])
                
                xAvg = (self.filteredPoint[8][0] + self.filteredPoint[12][0])/2
                yAvg = (self.filteredPoint[8][1] + self.filteredPoint[12][1])/2
                zAvg = (self.filteredPoint[8][2] + self.filteredPoint[12][2])/2
            
                #If thumb is touching index finger second landmark
                if dist < 4:
                    if not self.delete:
                        instruction += "Remove:"
                        self.delete = True
                else:
                    self.delete = False
                
                instruction += str(round(xAvg, 2)) + ";" + str(round(yAvg, 2)) + ";" + str(round(zAvg, 2))
            
            else:
                instruction = ""
                self.prevFilteredPoint = {4: None, 5: None, 8: None, 12: None}
            
        else:
            instruction = ""
            self.prevFilteredPoint = {4: None, 5: None, 8: None, 12: None}

        return instruction