from Writers.instructionWriter import InstructionWriter
import math

class MenuHandler(InstructionWriter):
    
    numModes = 6
    
    def __init__(self, inInstructionHandleValueSeparator, modeMask):
        super().__init__(inInstructionHandleValueSeparator, modeMask)

        self.menu = False
        self.modeShown = 0
        self.modeCurrent = 0
        
        self.xAvgInit = None
        self.yAvgInit = None
        
        self.filteredPoints = {}

    def generateInstruction(self, detector, trackObjs, camCalib):
        instruction = "Menu" + self.inInstructionHandleValueSeparator

        if len(trackObjs) > 0:
            hand = trackObjs[0]

            # If only index and middle fingers are up
            if hand["fingersUp"] == [0, 1, 1, 0, 0]:
                lmList = hand["lmList"]
                
                for id in (8, 12):
                    x = (lmList[id][0] - camCalib.w/2) * hand["px2cmRate"][0]
                    y = (-lmList[id][1] + camCalib.h/2) * hand["px2cmRate"][1]
                    z = lmList[id][2] * hand["px2cmRate"][2] + hand["tVec"][2]
                    
                    if id not in self.filteredPoints:
                        self.filteredPoints[id] = (x, y, z)
                    
                    self.filteredPoints[id] = InstructionWriter.filterPointEWA((x, y, z), self.filteredPoints[id])
                
                dist = math.hypot(self.filteredPoints[8][0] - self.filteredPoints[12][0], self.filteredPoints[8][1] - self.filteredPoints[12][1], self.filteredPoints[8][2] - self.filteredPoints[12][2])
                
                xAvg = (self.filteredPoints[8][0] + self.filteredPoints[12][0])/2
                yAvg = (self.filteredPoints[8][1] + self.filteredPoints[12][1])/2
                
                #If index and middle fingers are close
                if dist < 4:
                    if self.yAvgInit is None:
                        self.yAvgInit = yAvg
                    yDelta = yAvg - self.yAvgInit
                    
                    if not self.menu:
                        if yDelta < -3:
                            self.menu = True
                            self.yAvgInit = yAvg

                        instruction = ""

                    else:
                        if self.xAvgInit is None:
                            self.xAvgInit = xAvg
                        xDelta = xAvg - self.xAvgInit
                        
                        if xDelta < 0:
                            self.xAvgInit = xAvg
                            
                        if xDelta > 3:
                            self.modeCurrent = self.modeShown
                            self.menu = False
                            self.yAvgInit = None
                            self.xAvgInit = None
                            instruction += "Selected:" + str(self.modeCurrent)                        
                        else:
                            if yDelta < -1.5:
                                self.modeShown = (self.modeShown - 1 ) % MenuHandler.numModes
                                self.yAvgInit = yAvg - 1.5
                                self.xAvgInit = xAvg
                            if yDelta > 1.5:
                                self.modeShown = (self.modeShown + 1) % MenuHandler.numModes
                                self.yAvgInit = yAvg + 1.5
                                self.xAvgInit = xAvg
                            
                            yDelta = yAvg - self.yAvgInit
                            percentage = (50*yDelta/1.5)
                            instruction += str(self.modeShown) + ";" + str(round(percentage,2))

                else:
                    instruction = ""
                    self.menu = 0
                    self.yAvgInit = None
                    self.xAvgInit = None
                    self.filteredPoints = {}

            else:
                instruction = ""
                self.menu = 0
                self.yAvgInit = None
                self.xAvgInit = None
                self.filteredPoints = {}

        else:
            instruction = ""
            self.menu = 0
            self.yAvgInit = None
            self.xAvgInit = None
            self.filteredPoints = {}
 
        return instruction