from Writers.instructionWriter import InstructionWriter
import math

class FreeTransform(InstructionWriter):
    
    def __init__(self, inInstructionHandleValueSeparator):
        super().__init__(inInstructionHandleValueSeparator)

        self.free = False
        self.x0Init = 0
        self.y0Init = 0
        self.z0Init = 0
        self.x1Init = 0
        self.y1Init = 0
        self.z1Init = 0

    def generateInstruction(self, detector, trackObjs, camCalib):
        instruction = "Free" + self.inInstructionHandleValueSeparator

        if len(trackObjs) == 2:
            hand0 = trackObjs[0]
            hand1 = trackObjs[1]
            
            #Free
            if hand0["fingersUp"] == [1, 1, 0, 0, 0] and hand1["fingersUp"] == [1, 1, 0, 0, 0]:
                lmList0 = hand0["lmList"]
                lmList1 = hand1["lmList"]

                x0_0 = (lmList0[4][0] - camCalib.w/2)*hand0["px2cmRate"][0]
                y0_0 = (-lmList0[4][1] + camCalib.h/2)*hand0["px2cmRate"][1]
                z0_0 = lmList0[4][2]*hand0["px2cmRate"][2] + hand0["tVec"][2]

                x1_0 = (lmList0[8][0] - camCalib.w/2)*hand0["px2cmRate"][0]
                y1_0 = (-lmList0[8][1] + camCalib.h/2)*hand0["px2cmRate"][1]
                z1_0 = lmList0[8][2]*hand0["px2cmRate"][2] + hand0["tVec"][2]

                x0_1 = (lmList1[4][0] - camCalib.w/2)*hand1["px2cmRate"][0]
                y0_1 = (-lmList1[4][1] + camCalib.h/2)*hand1["px2cmRate"][1]
                z0_1 = lmList1[4][2]*hand1["px2cmRate"][2] + hand1["tVec"][2]

                x1_1 = (lmList1[8][0] - camCalib.w/2)*hand1["px2cmRate"][0]
                y1_1 = (-lmList1[8][1] + camCalib.h/2)*hand1["px2cmRate"][1]
                z1_1 = lmList1[8][2]*hand1["px2cmRate"][2] + hand1["tVec"][2]

                dist0 = math.hypot(x0_0 - x1_0, y0_0 - y1_0, z0_0 - z1_0)
                dist1 = math.hypot(x0_1 - x1_1, y0_1 - y1_1, z0_1 - z1_1)

                #Both hands "picking" pose: thumb and index tips are close
                if dist0 < 4 and dist1 < 4:
                    xAvg = (x0_0 + x0_1)/2
                    yAvg = (y0_0 + y0_1)/2
                    zAvg = (z0_0 + z0_1)/2
                    if not self.free:
                        self.free = True
                        instruction += "Free" + ":" + str(xAvg) + ";" + str(yAvg) + ";" + str(zAvg)

                    #Instruction = delta of each hand
                    else:
                        xDelta0 = self.x0Init - x0_0
                        yDelta0 = self.y0Init - y0_0
                        zDelta0 = self.z0Init - z0_0
                        xDelta1 = self.x1Init - x0_1
                        yDelta1 = self.y1Init - y0_1
                        zDelta1 = self.z1Init - z0_1
                        instruction += str(xDelta0) + ";" + str(yDelta0) + ";" + str(zDelta0) + "/" + str(xDelta1) + ";" + str(yDelta1) + ";" + str(zDelta1)

                else:
                    if self.free:
                        instruction += "Cancel Free Transform"
                    else:
                        instruction = ""
                    self.free = False

            else:
                    if self.free:
                        instruction += "Cancel Free Transform"
                    else:
                        instruction = ""
                    self.free = False 

        else:
                    if self.free:
                        instruction += "Cancel Free Transform"
                    else:
                        instruction = ""
                    self.free = False   

        return instruction