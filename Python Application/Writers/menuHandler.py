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
        self.prevFilteredPoint = {8: None, 12: None}

    def generateInstruction(self, detector, trackObjs, camCalib):
        instruction = "Menu" + self.inInstructionHandleValueSeparator

        if len(trackObjs) > 0:
            hand = trackObjs[0]

            #If only index and middle fingers are up
            if hand["fingersUp"] == [0, 1, 1, 0, 0]:
                lmList = hand["lmList"]
                
                for id in (8, 12):
                    x = (lmList[id][0] - camCalib.w/2)*hand["px2cmRate"][0]
                    y = (-lmList[id][1] + camCalib.h/2)*hand["px2cmRate"][1]
                    z = lmList[id][2]*hand["px2cmRate"][2] + hand["tVec"][2]
                    
                    if self.filteredPoint[id] == None:
                        self.filteredPoint[id] = (x, y, z)
                    
                    InstructionWriter.filterPointEWA((x, y, z), self.filteredPoint[id])
                    
                    self.filteredPoint[id] = (x, y, z)
                
                dist = math.hypot(self.filteredPoint[8][0] - self.filteredPoint[12][0], self.filteredPoint[8][1] - self.filteredPoint[12][1], self.filteredPoint[8][2] - self.filteredPoint[12][2])
                
                xAvg = (self.filteredPoint[8][0] + self.filteredPoint[12][0])/2
                yAvg = (self.filteredPoint[8][1] + self.filteredPoint[12][1])/2
                
                #If index and middle fingers are close
                if dist < 5:
                    if self.yAvgInit is None:
                        self.yAvgInit = yAvg
                        self.yLastPos = yAvg
                    yPos = (self.beta*self.yLastPos + (1-self.beta)*yAvg)
                    self.yLastPos = yPos
                    yDelta = self.yAvgInit - yPos
                    
                    if not self.menu:
                        if yDelta > 3:
                            self.menu = True
                            self.yAvgInit = yAvg

                        instruction = ""

                    else:
                        if self.xAvgInit is None:
                            self.xAvgInit = xAvg
                            self.xLastPos = xAvg
                        xPos = (self.beta*self.xLastPos + (1-self.beta)*xAvg)
                        self.xLastPos = xPos
                        xDelta = self.xAvgInit - xPos
                        percentage = round(50*yDelta/3)
                        
                        if xDelta < 0:
                            self.xAvgInit = xAvg
                        if xDelta > 3:
                            self.modeCurrent = self.modeShown
                            self.menu = False
                            self.yAvgInit = None
                            self.xAvgInit = None
                            instruction += "Selected:" + str(self.modeCurrent)
                                                       
                        else:
                            if yDelta < 3:
                                self.modeShown = (self.modeShown + 1) % 4
                                self.yAvgInit = yAvg + 1.5
                                self.xAvgInit = xAvg
                            if yDelta > -3:
                                self.modeShown = (self.modeShown - 1) % 4
                                self.yAvgInit = yAvg - 1.5
                                self.xAvgInit = xAvg
                            instruction += str(self.modeShown) + ";" + str(percentage)

                else:
                    instruction = ""
                    self.menu = 0
                    self.yAvgInit = None
                    self.xAvgInit = None
                    self.prevFilteredPoint = {8: None, 12: None}

            else:
                instruction = ""
                self.menu = 0
                self.yAvgInit = None
                self.xAvgInit = None
                self.prevFilteredPoint = {8: None, 12: None}

        else:
            instruction = ""
            self.menu = 0
            self.yAvgInit = None
            self.xAvgInit = None
            self.prevFilteredPoint = {8: None, 12: None}
 
        return instruction