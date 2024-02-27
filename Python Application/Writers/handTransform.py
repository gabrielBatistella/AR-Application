from Writers.instructionWriter import InstructionWriter
import math

class HandTransform(InstructionWriter):
    
    def __init__(self, inInstructionHandleValueSeparator):
        super().__init__(inInstructionHandleValueSeparator)

        self.scale = False
        self.scaleDistance = None
        self.hold = False
        self.rotate = False
        self.xAvgInit = 0
        self.yAvgInit = 0
        self.zAvgInit = 0

    def generateInstruction(self, detector, trackObjs, camCalib):
        instruction = "Transform" + self.inInstructionHandleValueSeparator

        if len(trackObjs) == 2:
            hand0 = trackObjs[0]
            hand1 = trackObjs[1]

            #Scale
            if hand0["fingersUp"] == [1, 1, 0, 0, 0] and hand1["fingersUp"] == [1, 1, 0, 0, 0]:
                lmList0 = hand0["lmList"]
                lmList1 = hand1["lmList"]

                x0 = (lmList0[5][0] - camCalib.w/2)*hand["px2cmRate"][0]
                y0 = (-lmList0[5][1] + camCalib.h/2)*hand["px2cmRate"][1]
                z0 = lmList0[5][2]*hand["px2cmRate"][2] + hand["tVec"][2]

                x1 = (lmList1[5][0] - camCalib.w/2)*hand["px2cmRate"][0]
                y1 = (-lmList1[5][1] + camCalib.h/2)*hand["px2cmRate"][1]
                z0 = lmList1[5][2]*hand["px2cmRate"][2] + hand["tVec"][2]

                dist = math.hypot(x1 - x0, y1 - y0, z1 - z0)

                #Define original scale as distance between landmark 5 of hands
                if not self.scale:
                    xAvg = (x0 + x1)/2
                    yAvg = (y0 + y1)/2
                    zAvg = (z0 + z1)/2
                    self.scaleDistance = dist
                    self.scale = True
                    instruction += "Scale" + ":" + str(xAvg) + ";" + str(yAvg) + ";" + str(zAvg)

                else:
                    scale = round(dist/self.scaleDistance)
                    instruction += str(scale)

            else:
                if self.scale:
                    instruction += "Stop Scaling"
                else:
                    instruction = ""
                self.scale = False
                self.scaleDistance = None       

        elif len(trackObjs) == 1:
            hand = trackObjs[0]

            #Hold
            if hand["fingersUp"] == [1, 1, 0, 0, 0]:
                lmList = hand["lmList"]
                
                x0 = (lmList[4][0] - camCalib.w/2)*hand["px2cmRate"][0]
                y0 = (-lmList[4][1] + camCalib.h/2)*hand["px2cmRate"][1]
                z0 = lmList[4][2]*hand["px2cmRate"][2] + hand["tVec"][2]
                
                x1 = (lmList[8][0] - camCalib.w/2)*hand["px2cmRate"][0]
                y1 = (-lmList[8][1] + camCalib.h/2)*hand["px2cmRate"][1]
                z1 = lmList[8][2]*hand["px2cmRate"][2] + hand["tVec"][2]
                
                dist = math.hypot(x1 - x0, y1 - y0, z1 - z0)
                
                #If thumb and index finger are close
                if dist < 4:
                    xAvg = (x0 + x1)/2
                    yAvg = (y0 + y1)/2
                    zAvg = (z0 + z1)/2
                    
                    if not self.hold:
                        instruction += "Hold" + ":" + str(xAvg) + ";" + str(yAvg) + ";" + str(zAvg)
                        self.xAvgInit = xAvg
                        self.yAvgInit = yAvg
                        self.zAvgInit = zAvg
                        self.hold = True
                    
                    else:
                        xDelta = self.xAvgInit - xAvg
                        yDelta = self.yAvgInit - yAvg
                        zDelta = self.zAvgInit - zAvg
                        instruction += str(xDelta) + ";" + str(yDelta) + ";" + str(zDelta)

                else:
                    if self.hold:
                        instruction += "Release"
                    else:
                        instruction = ""
                    self.hold = False
            else:
                    if self.hold:
                        instruction += "Release"
                    else:
                        instruction = ""
                    self.hold = False

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
                
                #If thumb is touching index finger second landmark
                if dist < 4:
                    xAvg = (x0 + x1)/2
                    yAvg = (y0 + y1)/2
                    zAvg = (z0 + z1)/2
                    
                    if not self.rotate:
                        instruction += "Rotate" + ":" + str(xAvg) + ";" + str(yAvg) + ";" + str(zAvg)
                        self.xAvgInit = xAvg
                        self.yAvgInit = yAvg
                        self.zAvgInit = zAvg
                        self.rotate = True
                    
                    else:
                        rollDelta = round((self.xAvgInit - xAvg)/4*360)
                        pitchDelta = round((self.yAvgInit - yAvg)/4*360)
                        yawDelta = round((self.zAvgInit - zAvg)/4*360)
                        instruction += str(rollDelta) + ";" + str(pitchDelta) + ";" + str(yawDelta)

                else:
                    if self.rotate:
                        instruction += "Stop Rotating"
                    else:
                        instruction = ""
                    self.rotate = False
            else:
                    if self.rotate:
                        instruction += "Stop Rotating"
                    else:
                        instruction = ""
                    self.hold = False
                    self.rotate = False
            
        else:
                if self.hold:
                    instruction += "Release"
                elif self.rotate:
                    instruction += "Stop Rotating"
                elif self.scale:
                    instruction += "Stop Scaling"
                else:
                    instruction = ""
                self.hold = False
                self.rotate = False
                self.scale = False

        return instruction
