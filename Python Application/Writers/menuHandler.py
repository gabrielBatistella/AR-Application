from Writers.instructionWriter import InstructionWriter
import math

class MenuHandler(InstructionWriter):
    
    def __init__(self, inInstructionHandleValueSeparator, modeMask):
        super().__init__(inInstructionHandleValueSeparator, modeMask)

        self.menu = False
        self.loading = False
        self.modeShown = 0
        self.modeCurrent = 0
        self.xAvgInit = None
        self.yAvgInit = None

    def getDisableInstruction(self):
        instruction = "Menu" + self.inInstructionHandleValueSeparator
        instruction += "Close Menu"
        return instruction

    def generateInstruction(self, detector, trackObjs, camCalib):
        instruction = "Menu" + self.inInstructionHandleValueSeparator

        if len(trackObjs) > 0:
            hand = trackObjs[0]

            #If only index and middle fingers are up
            if hand["fingersUp"] == [0, 1, 1, 0, 0]:
                lmList = hand["lmList"]
                
                x1 = (lmList[8][0] - camCalib.w/2)*hand["px2cmRate"][0]
                y1 = (-lmList[8][1] + camCalib.h/2)*hand["px2cmRate"][1]
                z1 = lmList[8][2]*hand["px2cmRate"][2] + hand["tVec"][2]
                
                x2 = (lmList[12][0] - camCalib.w/2)*hand["px2cmRate"][0]
                y2 = (-lmList[12][1] + camCalib.h/2)*hand["px2cmRate"][1]
                z2 = lmList[12][2]*hand["px2cmRate"][2] + hand["tVec"][2]
                
                dist = math.hypot(x2 - x1, y2 - y1, z2 - z1)
                
                #If index and middle fingers are close
                if dist < 5:
                    yAvg = (y1+y2)/2

                    if not self.menu:
                        if self.yAvgInit is None:
                            self.yAvgInit = yAvg
                        
                        yDelta = self.yAvgInit - yAvg
                        if yDelta > 3:
                            self.menu = True
                            self.yAvgInit = yAvg

                        instruction = ""

                    else:
                        xAvg = (x1+x2)/2
                        
                        if self.xAvgInit is None:
                            self.xAvgInit = xAvg
                    
                        yDelta = yAvg - self.yAvgInit
                        xDelta = xAvg - self.xAvgInit
                        percentage = round(50*yDelta/4)
                        
                        #If fingers move to right, resets initial x value
                        #If fingers move to left, enter the mode shown
                        #If fingers move up or down, changes the modes shown
                        if xDelta < 0:
                            self.xAvgInit = xAvg
                        if xDelta > 3:
                            self.modeCurrent = self.modeShown
                            self.menu = False
                            self.yAvgInit = None
                            self.xAvgInit = None
                            instruction += "Selected:" + str(self.modeCurrent)
                        
                        #Modes: 0)Calibrate (followFingerTips) 1)Move, Rotate and Zoom 2)Spawn and Delete 4)???                                
                        else:
                            if yDelta > 4:
                                self.modeShown = (self.modeShown + 1) % 4
                                self.yAvgInit = yAvg + 2
                                self.xAvgInit = xAvg
                            if yDelta < -4:
                                self.modeShown = (self.modeShown - 1) % 4
                                self.yAvgInit = yAvg - 2
                                self.xAvgInit = xAvg
                            instruction += str(self.modeShown) + ";" + str(percentage)

                else:
                    if self.menu:
                        instruction += "Close Menu"
                    else:
                        instruction = ""
                    self.menu = 0
                    self.yAvgInit = None
                    self.xAvgInit = None

            else:
                if self.menu:
                    instruction += "Close Menu"
                else:
                    instruction = ""
                self.menu = 0
                self.yAvgInit = None
                self.xAvgInit = None

        else:
            if self.menu:
                instruction += "Close Menu"
            else:
                instruction = ""
            self.menu = 0
            self.yAvgInit = None
            self.xAvgInit = None
         
        return instruction