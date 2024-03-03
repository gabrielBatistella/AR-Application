from Writers.instructionWriter import InstructionWriter
import math

class ObjectScaler(InstructionWriter):
    
    def __init__(self, inInstructionHandleValueSeparator, modeMask):
        super().__init__(inInstructionHandleValueSeparator, modeMask)

        self.holding = False
        self.following = False
        self.xAvgInit = 0

    def getDisableInstruction(self):
        instruction = "Scale" + self.inInstructionHandleValueSeparator
        instruction += "Lost Track"
        return instruction

    def generateInstruction(self, detector, trackObjs, camCalib):
        instruction = "Scale" + self.inInstructionHandleValueSeparator

        if len(trackObjs) > 0:
            hand = trackObjs[0]

            #Scale
            if hand["fingersUp"] == [1, 1, 1, 1, 1]:
                lmList = hand["lmList"]
                
                x0 = (lmList[4][0] - camCalib.w/2)*hand["px2cmRate"][0]
                y0 = (-lmList[4][1] + camCalib.h/2)*hand["px2cmRate"][1]
                z0 = lmList[4][2]*hand["px2cmRate"][2] + hand["tVec"][2]
                
                x1 = (lmList[8][0] - camCalib.w/2)*hand["px2cmRate"][0]
                y1 = (-lmList[8][1] + camCalib.h/2)*hand["px2cmRate"][1]
                z1 = lmList[8][2]*hand["px2cmRate"][2] + hand["tVec"][2]
                
                dist = math.hypot(x1 - x0, y1 - y0, z1 - z0)
                
                xAvg = (x0 + x1)/2
                yAvg = (y0 + y1)/2
                zAvg = (z0 + z1)/2
                
                if dist < 4:
                    if not self.holding:
                        self.holding = True
                        self.xAvgInit = xAvg
                        instruction += "Grab:" + str(xAvg) + ";" + str(yAvg) + ";" + str(zAvg)

                    else:
                        scale = abs(round((self.xAvgInit - xAvg)/3, 3))
                        instruction += "Holding:" + str(scale)

                else:
                    if self.holding:
                        instruction += "Release:"
                        self.holding = False
                    instruction += str(xAvg) + ";" + str(yAvg) + ";" + str(zAvg)       
                
                self.following = True
                
            else:
                if self.following:
                    instruction += "Lost Track"
                    self.holding = False
                    self.following = False
                else:
                    instruction = ""

        else:
            if self.following:
                instruction += "Lost Track"
                self.holding = False
                self.following = False
            else:
                instruction = ""
                
        return instruction
