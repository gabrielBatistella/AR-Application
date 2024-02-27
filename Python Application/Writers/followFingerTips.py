from Writers.instructionWriter import InstructionWriter

class FollowFingerTips(InstructionWriter):

    def __init__(self, inInstructionHandleValueSeparator):
        super().__init__(inInstructionHandleValueSeparator)

        self.following = False

    def generateInstruction(self, detector, trackObjs, camCalib):
        instruction = "FingerPos" + self.inInstructionHandleValueSeparator

        if len(trackObjs) > 0:
            hand = trackObjs[0]
            fingerTipLm = hand["lmList"][detector.tipIds]
            
            x0 = round((fingerTipLm[0][0] - camCalib.w/2)*hand["px2cmRate"][0],2)
            y0 = round((-fingerTipLm[0][1] + camCalib.h/2)*hand["px2cmRate"][1],2)
            z0 = round(fingerTipLm[0][2]*hand["px2cmRate"][2] + hand["tVec"][2],2)

            x1 = round((fingerTipLm[1][0] - camCalib.w/2)*hand["px2cmRate"][0],2)
            y1 = round((-fingerTipLm[1][1] + camCalib.h/2)*hand["px2cmRate"][1],2)
            z1 = round(fingerTipLm[1][2]*hand["px2cmRate"][2] + hand["tVec"][2],2)

            x2 = round((fingerTipLm[2][0] - camCalib.w/2)*hand["px2cmRate"][0],2)
            y2 = round((-fingerTipLm[2][1] + camCalib.h/2)*hand["px2cmRate"][1],2)
            z2 = round(fingerTipLm[2][2]*hand["px2cmRate"][2] + hand["tVec"][2],2)

            x3 = round((fingerTipLm[3][0] - camCalib.w/2)*hand["px2cmRate"][0],2)
            y3 = round((-fingerTipLm[3][1] + camCalib.h/2)*hand["px2cmRate"][1],2)
            z3 = round(fingerTipLm[3][2]*hand["px2cmRate"][2] + hand["tVec"][2],2)

            x4 = round((fingerTipLm[4][0] - camCalib.w/2)*hand["px2cmRate"][0],2)
            y4 = round((-fingerTipLm[4][1] + camCalib.h/2)*hand["px2cmRate"][1],2)
            z4 = round(fingerTipLm[4][2]*hand["px2cmRate"][2] + hand["tVec"][2],2)

            instruction += str(x0) + ";" + str(y0) + ";" + str(z0) + "/" + str(x1) + ";" + str(y1) + ";" + str(z1) + "/" + str(x2) + ";" + str(y2) + ";" + str(z2) + "/" + str(x3) + ";" + str(y3) + ";" + str(z3) + "/" + str(x4) + ";" + str(y4) + ";" + str(z4)
            self.following = True

        else:
            if self.following:
                instruction += "Lost Track"
                self.following = False
            else:
                instruction = ""

        return instruction