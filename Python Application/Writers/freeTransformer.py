from Writers.instructionWriter import InstructionWriter
import math

class FreeTransformer(InstructionWriter):
    
    def __init__(self, inInstructionHandleValueSeparator, modeMask):
        super().__init__(inInstructionHandleValueSeparator, modeMask)

        self.leftHolding = False
        self.leftFollowing = False
        self.rightHolding = False
        self.rightFollowing = False

    def getDisableInstruction(self):
        instruction = "Free" + self.inInstructionHandleValueSeparator
        instruction += "Lost Track/Lost Track"
        return instruction

    def generateInstruction(self, detector, trackObjs, camCalib):
        instruction = "Free" + self.inInstructionHandleValueSeparator

        leftOn = False
        rightOn = False
        
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
        
                x0L = (lmListLeft[4][0] - camCalib.w/2)*leftHand["px2cmRate"][0]
                y0L = (-lmListLeft[4][1] + camCalib.h/2)*leftHand["px2cmRate"][1]
                z0L = lmListLeft[4][2]*leftHand["px2cmRate"][2] + leftHand["tVec"][2]

                x1L = (lmListLeft[8][0] - camCalib.w/2)*leftHand["px2cmRate"][0]
                y1L = (-lmListLeft[8][1] + camCalib.h/2)*leftHand["px2cmRate"][1]
                z1L = lmListLeft[8][2]*leftHand["px2cmRate"][2] + leftHand["tVec"][2]
                
                distL = math.hypot(x0L - x1L, y0L - y1L, z0L - z1L)
                
                xLAvg = (x0L + x1L)/2
                yLAvg = (y0L + y1L)/2
                zLAvg = (z0L + z1L)/2
                
                leftPos = ""

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
                        
                self.leftFollowing = True
                        
                leftPos += str(xLAvg) + ";" + str(yLAvg) + ";" + str(zLAvg)
            
            else:
                if self.leftFollowing:
                    leftPos = "Lost Track"
                    self.leftHolding = False
                    self.leftFollowing = False
                else:
                    leftPos = "None"
                
            if rightOn:
                lmListRight = rightHand["lmList"]
                x0R = (lmListRight[4][0] - camCalib.w/2)*rightHand["px2cmRate"][0]
                y0R = (-lmListRight[4][1] + camCalib.h/2)*rightHand["px2cmRate"][1]
                z0R = lmListRight[4][2]*rightHand["px2cmRate"][2] + rightHand["tVec"][2]

                x1R = (lmListRight[8][0] - camCalib.w/2)*rightHand["px2cmRate"][0]
                y1R = (-lmListRight[8][1] + camCalib.h/2)*rightHand["px2cmRate"][1]
                z1R = lmListRight[8][2]*rightHand["px2cmRate"][2] + rightHand["tVec"][2]

                distR = math.hypot(x0R - x1R, y0R - y1R, z0R - z1R)
                
                xRAvg = (x0R + x1R)/2
                yRAvg = (y0R + y1R)/2
                zRAvg = (z0R + z1R)/2
                
                rightPos = ""

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
                        
                self.rightFollowing = True
                        
                rightPos += str(xRAvg) + ";" + str(yRAvg) + ";" + str(zRAvg)
            
            else:
                if self.rightFollowing:
                    rightPos = "Lost Track"
                    self.rightHolding = False
                    self.rightFollowing = False
                else:
                    rightPos = "None"
        
        if leftPos == "None" and rightPos =="None":
            instruction = ""
        else:
            instruction += leftPos + "/" + rightPos
            
        return instruction