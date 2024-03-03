from Writers.instructionWriter import InstructionWriter
import math

class ObjectRotator(InstructionWriter):
    
    def __init__(self, inInstructionHandleValueSeparator, modeMask):
        super().__init__(inInstructionHandleValueSeparator, modeMask)

        self.holding = False
        self.following = False
        self.xAvgInit = 0
        self.yAvgInit = 0
        self.zAvgInit = 0

    def getDisableInstruction(self):
        instruction = "Rotate" + self.inInstructionHandleValueSeparator
        instruction += "Lost Track"
        return instruction

    def generateInstruction(self, detector, trackObjs, camCalib):
        instruction = "Rotate" + self.inInstructionHandleValueSeparator

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
                
                x2 = (lmList[8][0] - camCalib.w/2)*hand["px2cmRate"][0]
                y2 = (-lmList[8][1] + camCalib.h/2)*hand["px2cmRate"][1]
                z2 = lmList[8][2]*hand["px2cmRate"][2] + hand["tVec"][2]
                
                x3 = (lmList[12][0] - camCalib.w/2)*hand["px2cmRate"][0]
                y3 = (-lmList[12][1] + camCalib.h/2)*hand["px2cmRate"][1]
                z3 = lmList[12][2]*hand["px2cmRate"][2] + hand["tVec"][2]
                
                dist = math.hypot(x3 - x2, y3 - y2, z3 - z2)
                
                xAvg = (x2 + x3)/2
                yAvg = (y2 + y3)/2
                zAvg = (z2 + z3)/2
            
                #If thumb is touching index finger second landmark
                if dist < 4:
                    if not self.holding:
                        self.xAvgInit = xAvg
                        self.yAvgInit = yAvg
                        self.zAvgInit = zAvg
                        self.holding = True
                        instruction += "Grab:" + str(xAvg) + ";" + str(yAvg) + ";" + str(zAvg)
                    else:
                        rollDelta = round((self.xAvgInit - xAvg)/4*360)
                        pitchDelta = round((self.yAvgInit - yAvg)/4*360)
                        yawDelta = round((self.zAvgInit - zAvg)/4*360)
                        instruction += "Holding:" + str(rollDelta) + ";" + str(pitchDelta) + ";" + str(yawDelta)
                    
                    self.following = True

                else:
                    if self.holding:
                        instruction += "Release:"
                        self.holding = False
                    instruction += str(xAvg) + ";" + str(yAvg) + ";" + str(zAvg)

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