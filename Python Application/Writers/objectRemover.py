from Writers.instructionWriter import InstructionWriter
import math

class ObjectRemover(InstructionWriter):
    
    def __init__(self, inInstructionHandleValueSeparator, modeMask):
        super().__init__(inInstructionHandleValueSeparator, modeMask)

        self.delete = False

    def getDisableInstruction(self):
        instruction = "Remove" + self.inInstructionHandleValueSeparator
        instruction += "Lost Track"
        return instruction

    def generateInstruction(self, detector, trackObjs, camCalib):
        instruction = "Remove" + self.inInstructionHandleValueSeparator

        if len(trackObjs) > 0:
            hand = trackObjs[0]

            #Rotate
            if hand["fingersUp"] == [1, 1, 1, 0, 0]:
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
            
                #If thumb is touching index finger second landmark
                if dist < 4:
                    
                    if not self.delete:
                        instruction += "Remove:"
                        self.delete = True
                    instruction += str(xAvg) + ";" + str(yAvg) + ";" + str(zAvg)

                else:
                    self.delete = False
                    instruction += str(xAvg) + ";" + str(yAvg) + ";" + str(zAvg)

            else:
                if self.delete:
                    instruction += "Lost Track"
                    self.delete = False
                else:
                    instruction = ""
            
        else:
            if self.delete:
                instruction += "Lost Track"
                self.delete = False
            else:
                instruction = ""

        return instruction