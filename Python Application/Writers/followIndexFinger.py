from Writers.instructionWriter import InstructionWriter

class FollowIndexFinger(InstructionWriter):

    def __init__(self, inInstructionHandleValueSeparator):
        super().__init__(inInstructionHandleValueSeparator)

        self.following = False

    def generateInstruction(self, detector, trackObjs, camCalib):
        instruction = "FingerPos" + self.inInstructionHandleValueSeparator

        if len(trackObjs) > 0:
            hand = trackObjs[0]

            fingerLm = hand["lmList"][detector.tipIds[1]]
            hDist = (fingerLm[0] - camCalib.w/2)*hand["px2cmRate"][0]
            vDist = (-fingerLm[1] + camCalib.h/2)*hand["px2cmRate"][1]
            pDist = fingerLm[2]*hand["px2cmRate"][2] + hand["tVec"][2]

            instruction += str(round(hDist, 2)) + ";" + str(round(vDist, 2)) + ";" + str(round(pDist, 2))
            self.following = True

        else:
            if self.following:
                instruction += "Lost Track"
                self.following = False
            else:
                instruction = ""

        return instruction