from Writers.instructionWriter import InstructionWriter
import math

class HandScale(InstructionWriter):
    
    def __init__(self, inInstructionHandleValueSeparator):
        super().__init__(inInstructionHandleValueSeparator)

        self.scale = False
        self.scaleDistance = None

    def generateInstruction(self, detector, trackObjs, camCalib):
        instruction = "Scale" + self.inInstructionHandleValueSeparator

        if len(trackObjs) == 2:
            hand0 = trackObjs[0]
            hand1 = trackObjs[1]

            lmList0 = hand0["lmList"]
            lmList1 = hand1["lmList"]

            x0 = (lmList0[5][0] - camCalib.w/2)*hand0["px2cmRate"][0]
            y0 = (-lmList0[5][1] + camCalib.h/2)*hand0["px2cmRate"][1]
            z0 = lmList0[5][2]*hand0["px2cmRate"][2] + hand0["tVec"][2]

            x1 = (lmList1[5][0] - camCalib.w/2)*hand1["px2cmRate"][0]
            y1 = (-lmList1[5][1] + camCalib.h/2)*hand1["px2cmRate"][1]
            z1 = lmList1[5][2]*hand1["px2cmRate"][2] + hand1["tVec"][2]

            dist = math.hypot(x1 - x0, y1 - y0, z1 - z0)
            
            xAvg = (x0 + x1)/2
            yAvg = (y0 + y1)/2
            zAvg = (z0 + z1)/2

            #Scale
            if hand0["fingersUp"] == [1, 1, 0, 0, 0] and hand1["fingersUp"] == [1, 1, 0, 0, 0]:

                #Define original scale as distance between landmark "5" of both hands
                if not self.scale:
                    self.scaleDistance = dist
                    self.scale = True
                    instruction += "Scale" + ":" + str(xAvg) + ";" + str(yAvg) + ";" + str(zAvg)

                else:
                    scale = round(dist/self.scaleDistance)
                    instruction += str(scale)

            else:
                if self.scale:
                    instruction += "Stop"
                    self.scale = False
                    self.scaleDistance = None
                else:
                    instruction += str(xAvg) + ";" + str(yAvg) + ";" + str(zAvg)       
            
        else:
            if self.scale:
                instruction += "Stop"
                self.scale = False
            else:
                instruction = ""
            

        return instruction
