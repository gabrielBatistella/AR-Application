from Writers.instructionWriter import InstructionWriter
import math

class FreeTransformer(InstructionWriter):
    
    def __init__(self, inInstructionHandleValueSeparator, modeMask):
        super().__init__(inInstructionHandleValueSeparator, modeMask)

        self.leftHolding = False
        self.rightHolding = False
        
        self.filteredPointsLeft = {}
        self.filteredPointsRight = {}

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

                for id in (4, 8):
                    x = (lmListLeft[id][0] - camCalib.w/2)*leftHand["px2cmRate"][0]
                    y = (-lmListLeft[id][1] + camCalib.h/2)*leftHand["px2cmRate"][1]
                    z = lmListLeft[id][2]*leftHand["px2cmRate"][2] + leftHand["tVec"][2]
                    
                    if id not in self.filteredPointsLeft:
                        self.filteredPointsLeft[id] = (x, y, z)

                    self.filteredPointsLeft[id] = InstructionWriter.filterPointEWA((x, y, z), self.filteredPointsLeft[id])
                
                distL = math.hypot(self.filteredPointsLeft[4][0] - self.filteredPointsLeft[8][0], self.filteredPointsLeft[4][1] - self.filteredPointsLeft[8][1], self.filteredPointsLeft[4][2] - self.filteredPointsLeft[8][2])
                
                xLAvg = (self.filteredPointsLeft[4][0] + self.filteredPointsLeft[8][0])/2
                yLAvg = (self.filteredPointsLeft[4][1] + self.filteredPointsLeft[8][1])/2
                zLAvg = (self.filteredPointsLeft[4][2] + self.filteredPointsLeft[8][2])/2

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
                
                for id in (4, 8):
                    x = (lmListRight[id][0] - camCalib.w/2)*rightHand["px2cmRate"][0]
                    y = (-lmListRight[id][1] + camCalib.h/2)*rightHand["px2cmRate"][1]
                    z = lmListRight[id][2]*rightHand["px2cmRate"][2] + rightHand["tVec"][2]
                    
                    if id not in self.filteredPointsRight:
                        self.filteredPointsRight[id] = (x, y, z)
                    
                    self.filteredPointsRight[id] = InstructionWriter.filterPointEWA((x, y, z), self.filteredPointsRight[id])
                
                distR = math.hypot(self.filteredPointsRight[4][0] - self.filteredPointsRight[8][0], self.filteredPointsRight[4][1] - self.filteredPointsRight[8][1], self.filteredPointsRight[4][2] - self.filteredPointsRight[8][2])
                
                xRAvg = (self.filteredPointsRight[4][0] + self.filteredPointsRight[8][0])/2
                yRAvg = (self.filteredPointsRight[4][1] + self.filteredPointsRight[8][1])/2
                zRAvg = (self.filteredPointsRight[4][2] + self.filteredPointsRight[8][2])/2
                
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
            self.leftHolding = False
            instruction = ""
            
            self.filteredPointsLeft = {}
            self.filteredPointsRight = {}

        return instruction