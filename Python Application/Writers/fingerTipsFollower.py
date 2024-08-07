from Writers.instructionWriter import InstructionWriter

class FingerTipsFollower(InstructionWriter):

    def __init__(self, inInstructionHandleValueSeparator, modeMask):
        super().__init__(inInstructionHandleValueSeparator, modeMask)

        self.filteredPoints = {}

    def generateInstruction(self, detector, trackObjs, camCalib):
        instruction = "FingerTips" + self.inInstructionHandleValueSeparator

        if len(trackObjs) > 0:
            hand = trackObjs[0]
            lmList = hand["lmList"]

            for id in (4, 8, 12, 16, 20):
                x = (lmList[id][0] - camCalib.w/2)*hand["px2cmRate"][0]
                y = (-lmList[id][1] + camCalib.h/2)*hand["px2cmRate"][1]
                z = lmList[id][2]*hand["px2cmRate"][2] + hand["tVec"][2]
                
                if id not in self.filteredPoints:
                    self.filteredPoints[id] = (x, y, z)
                
                self.filteredPoints[id] = InstructionWriter.filterPointEWA((x, y, z), self.filteredPoints[id])
                
                instruction += str(round(self.filteredPoints[id][0], 2)) + ";" + str(round(self.filteredPoints[id][1], 2)) + ";" + str(round(self.filteredPoints[id][2], 2)) + "/"

            instruction = instruction[:-1]
            
        else:
            instruction = ""
            self.filteredPoints = {}

        return instruction