from Writers.instructionWriter import InstructionWriter

class FollowIndexFinger(InstructionWriter):

    def __init__(self, inInstructionHandleValueSeparator):
        super().__init__(inInstructionHandleValueSeparator)

        self.following = False

    def generateInstruction(self, detector, trackObjs, camCalib):
        instruction = "FingerPos" + self.inInstructionHandleValueSeparator

        if len(trackObjs) > 0:
            hand = trackObjs[0]

            px2cmRate_x = hand["tVec"][0]/(hand["lmList"][0][0] - camCalib.w/2)
            px2cmRate_y = -hand["tVec"][1]/(-hand["lmList"][0][1] + camCalib.h/2)
            px2cmRate_z = px2cmRate_x

            fingerLm = hand["lmList"][detector.tipIds[1]]
            hDist = (fingerLm[0] - camCalib.w/2)*px2cmRate_x
            vDist = (-fingerLm[1] + camCalib.h/2)*px2cmRate_y
            pDist = fingerLm[2]*px2cmRate_z + hand["tVec"][2]

            instruction += str(round(hDist, 2)) + ";" + str(round(vDist, 2)) + ";" + str(round(pDist, 2))
            self.following = True

        else:
            if self.following:
                instruction += "Lost Track"
                self.following = False
            else:
                instruction = ""

        return instruction