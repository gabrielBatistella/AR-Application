from Writers.instructionWriter import InstructionWriter
import math

class HandHold(InstructionWriter):
    
    def __init__(self, inInstructionHandleValueSeparator):
        super().__init__(inInstructionHandleValueSeparator)

        self.hold = False

    def generateInstruction(self, detector, trackObjs, camCalib):
        instruction = "Hold" + self.inInstructionHandleValueSeparator

        if len(trackObjs) > 0:
            hand = trackObjs[0]
            lmList = hand["lmList"]
            
            x1 = (lmList[4][0] - camCalib.w/2)*hand["px2cmRate"][0]
            y1 = (-lmList[4][1] + camCalib.h/2)*hand["px2cmRate"][1]
            z1 = lmList[4][2]*hand["px2cmRate"][2] + hand["tVec"][2]
            
            x2 = (lmList[8][0] - camCalib.w/2)*hand["px2cmRate"][0]
            y2 = (-lmList[8][1] + camCalib.h/2)*hand["px2cmRate"][1]
            z2 = lmList[8][2]*hand["px2cmRate"][2] + hand["tVec"][2]
            
            dist = math.hypot(x2 - x1, y2 - y1, z2 - z1)
            
            #If thumb and index finger are close
            if dist < 1:
                hold = True
              
            else:
                hold = False

            instruction += str(hold)
            self.handhold = True

        else:
            if self.handhold:
                instruction += "Stop Hold"
                #Unity solta o objeto
                self.handhold = False
            else:
                instruction = ""

        return instruction
