from Writers.instructionWriter import InstructionWriter
import math

class ObjectScaler(InstructionWriter):
    
    def __init__(self, inInstructionHandleValueSeparator, modeMask):
        super().__init__(inInstructionHandleValueSeparator, modeMask)

        self.holding = False
        self.scaleDistance = 0

    def generateInstruction(self, detector, trackObjs, camCalib):
        instruction = "Scale" + self.inInstructionHandleValueSeparator

        if len(trackObjs) > 0:
            hand = trackObjs[0]

            #Rotate
            if hand["fingersUp"] == [1, 1, 1, 1, 1]:
                lmList = hand["lmList"]
                
                x0 = (lmList[4][0] - camCalib.w/2)*hand["px2cmRate"][0]
                y0 = (-lmList[4][1] + camCalib.h/2)*hand["px2cmRate"][1]
                z0 = lmList[4][2]*hand["px2cmRate"][2] + hand["tVec"][2]
                
                x1 = (lmList[6][0] - camCalib.w/2)*hand["px2cmRate"][0]
                y1 = (-lmList[6][1] + camCalib.h/2)*hand["px2cmRate"][1]
                z1 = lmList[6][2]*hand["px2cmRate"][2] + hand["tVec"][2]
                
                dist = math.hypot(x1 - x0, y1 - y0, z1 - z0)
                
                xAvg = (x0 + x1)/2
                yAvg = (y0 + y1)/2
                zAvg = (z0 + z1)/2

                if not self.holding:
                    self.scaleDistance = dist
                    self.holding = True
                    instruction += "Grab:" + str(xAvg) + ";" + str(yAvg) + ";" + str(zAvg)

                else:
                    scale = round(dist/self.scaleDistance, 3)
                    instruction += "Holding:" + str(scale)

            else:
                if self.holding:
                    instruction += "Release:"
                    self.holding = False
                    self.scaleDistance = 0
                instruction += str(xAvg) + ";" + str(yAvg) + ";" + str(zAvg)       
            
        else:
            if self.holding:
                instruction += "Release:"
                self.holding = False
                self.scaleDistance = 0
            instruction += str(xAvg) + ";" + str(yAvg) + ";" + str(zAvg)  
            
        return instruction
