from Writers.instructionWriter import InstructionWriter
import math

class FreeTransformer(InstructionWriter):
    
    def __init__(self, inInstructionHandleValueSeparator, modeMask):
        super().__init__(inInstructionHandleValueSeparator, modeMask)

        self.leftHolding = False
        self.leftFollowing = False
        self.rightHolding = False
        self.rightFollowing = False
        self.prevFilteredPointLeft = {8: None, 12: None}
        self.prevFilteredPointRight = {8: None, 12: None}

    def generateInstruction(self, detector, trackObjs, camCalib):
        instruction = "Free" + self.inInstructionHandleValueSeparator

        leftOn = False
        rightOn = False
        leftPos = "None"
        rightPos = "None"
        
        if len(trackObjs) > 0:
            if trackObjs[0]["type"] == "Left":
                leftHand = trackObjs[0]
                if leftHand["fingersUp"] == [1, 1, 0, 0, 0]:
                    leftOn = True
                if len(trackObjs) == 2:
                    rightHand = trackObjs[1]
                    if rightHand["fingersUp"] == [1, 1, 0, 0, 0]:
                        rightOn = True
            else:
                rightHand = trackObjs[0]
                if rightHand["fingersUp"] == [1, 1, 0, 0, 0]:
                    rightOn = True
                if len(trackObjs) == 2:
                    leftHand = trackObjs[1]
                    if leftHand["fingersUp"] == [1, 1, 0, 0, 0]:
                       leftOn = True
                
            #Free
            if leftOn:
                lmListLeft = leftHand["lmList"]

                for id in (8, 12):
                    x = (lmListLeft[id][0] - camCalib.w/2)*leftHand["px2cmRate"][0]
                    y = (-lmListLeft[id][1] + camCalib.h/2)*leftHand["px2cmRate"][1]
                    z = lmListLeft[id][2]*leftHand["px2cmRate"][2] + leftHand["tVec"][2]
                    
                    if self.filteredPointLeft[id] == None:
                        self.filteredPointLeft[id] = (x, y, z)
                    
                    InstructionWriter.filterPointEWA((x, y, z), self.filteredPointLeft[id])
                    
                    self.filteredPointLeft[id] = (x, y, z)
                
                distL = math.hypot(self.filteredPointLeft[8][0] - self.filteredPointLeft[12][0], self.filteredPointLeft[8][1] - self.filteredPointLeft[12][1], self.filteredPointLeft[8][2] - self.filteredPointLeft[12][2])
                
                xLAvg = (self.filteredPointLeft[8][0] + self.filteredPointLeft[12][0])/2
                yLAvg = (self.filteredPointLeft[8][1] + self.filteredPointLeft[12][1])/2
                zLAvg = (self.filteredPointLeft[8][2] + self.filteredPointLeft[12][2])/2

                if distL < 4: 
                    if not self.leftHolding:
                        self.leftHolding = True
                        leftPos = "Grab:"
                    else:
                        leftPos = "Holding:"
                else:
                    if self.leftHolding:
                        self.leftHolding = False
                        leftPos = "Release:"
                    else:
                        leftPos = ""
                        
                leftPos += str(round(xLAvg, 2)) + ";" + str(round(yLAvg, 2)) + ";" + str(round(zLAvg, 2))
            
            if rightOn:
                lmListRight = rightHand["lmList"]
                
                for id in (8, 12):
                    x = (lmListRight[id][0] - camCalib.w/2)*rightHand["px2cmRate"][0]
                    y = (-lmListRight[id][1] + camCalib.h/2)*rightHand["px2cmRate"][1]
                    z = lmListRight[id][2]*rightHand["px2cmRate"][2] + rightHand["tVec"][2]
                    
                    if self.filteredPointRight[id] == None:
                        self.filteredPointRight[id] = (x, y, z)
                    
                    InstructionWriter.filterPointEWA((x, y, z), self.filteredPointRight[id])
                    
                    self.filteredPointRight[id] = (x, y, z)
                
                distR = math.hypot(self.filteredPointRight[8][0] - self.filteredPointRight[12][0], self.filteredPointRight[8][1] - self.filteredPointRight[12][1], self.filteredPointRight[8][2] - self.filteredPointRight[12][2])
                
                xRAvg = (self.filteredPointRight[8][0] + self.filteredPointRight[12][0])/2
                yRAvg = (self.filteredPointRight[8][1] + self.filteredPointRight[12][1])/2
                zRAvg = (self.filteredPointRight[8][2] + self.filteredPointRight[12][2])/2
                
                if distR < 4: 
                    if not self.rightHolding:
                        self.rightHolding = True
                        rightPos = "Grab:"
                    else:
                        rightPos = "Holding:"
                else:
                    if self.rightHolding:
                        self.rightHolding = False
                        rightPos = "Release:"
                    else:
                        rightPos = ""
                        
                rightPos += str(round(xRAvg, 2)) + ";" + str(round(yRAvg, 2)) + ";" + str(round(zRAvg, 2))
                
            instruction += leftPos + "/" + rightPos

        else:
            self.rightHolding = False
            self.rightFollowing = False
            instruction = ""

        return instruction