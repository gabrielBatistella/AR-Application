from Writers.instructionWriter import InstructionWriter
import math

class MenuHandler(InstructionWriter):
    
    def __init__(self, inInstructionHandleValueSeparator):
        super().__init__(inInstructionHandleValueSeparator)

        self.menu = False
        self.loading = False
        self.modeShown = 0
        self.modeCurrent = 0
        self.xAvgInit = 0
        self.yAvgInit = 0

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
                        if not self.loading:
                            self.yAvgInit = yAvg
                            self.loading = True
                    
                        else:
                            yDelta = self.yAvgInit - yAvg
                            #If hand moved down, will have short delay of 20 frames to show menu
                            if yDelta > 5:
                                self.menu = True
                                self.loading = False

                        instruction = ""
                    
                    #If menu = True, will show Menu UI in Unity
                    else:
                        xAvg = (x1+x2)/2
                        
                        if not self.loading:
                            self.yAvgInit = yAvg
                            self.xAvgInit = xAvg
                            self.loading = True

                            instruction = ""
                        
                        else:
                            yDelta = yAvg - self.yAvgInit
                            xDelta = xAvg - self.xAvgInit
                            percentage = round(50*yDelta/7)
                            #If fingers move to right, resets initial x value
                            #If fingers move to left, enter the mode shown
                            #If fingers move up or down, changes the modes shown
                            
                            if xDelta < 0:
                                self.xAvgInit = xAvg
                            if xDelta > 7:
                                self.modeCurrent = self.modeShown
                                self.menu = 0
                                self.loading = 0
                                instruction += "Selected " + str(self.modeCurrent)
                            
                            #Modes: 0)Calibrate (followFingerTips) 1)Move, Rotate and Zoom 2)Spawn and Delete 4)???                                
                            else:
                                if yDelta > 7:
                                    self.modeShown = (self.modeShown + 1) % 3
                                    self.loading = False
                                if yDelta < -7:
                                    self.modeShown = (self.modeShown - 1) % 3
                                    self.loading = False
                                instruction += str(self.modeShown) + ";" + str(percentage)

                else:
                    if self.menu:
                        instruction += "Close Menu"
                    else:
                        instruction = ""
                    self.menu = 0
                    self.loading = False
                    
                    
            else:
                if self.menu:
                    instruction += "Close Menu"
                else:
                    instruction = ""
                self.menu = 0
                self.loading = False

        else:
            if self.menu:
                instruction += "Close Menu"
            else:
                instruction = ""
            self.menu = 0
            self.loading = False
         
        return instruction