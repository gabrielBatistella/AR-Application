from Writers.instructionWriter import InstructionWriter

class FollowFingerTips(InstructionWriter):

    def __init__(self, inInstructionHandleValueSeparator):
        super().__init__(inInstructionHandleValueSeparator)

        self.following = False

    def generateInstruction(self, detector, trackObjs, camCalib):
        instruction = "FingerTips" + self.inInstructionHandleValueSeparator

        if len(trackObjs) > 0:
            hand = trackObjs[0]
            lmList = hand["lmList"]

            for id in detector.tipIds:
                x = round((lmList[id][0] - camCalib.w/2)*hand["px2cmRate"][0],2)
                y = round((-lmList[id][1] + camCalib.h/2)*hand["px2cmRate"][1],2)
                z = round(lmList[id][2]*hand["px2cmRate"][2] + hand["tVec"][2],2)

                instruction += str(x) + ";" + str(y) + ";" + str(z) + "/"

            instruction = instruction[:-1]

            self.following = True

        else:
            if self.following:
                instruction += "Lost Track"
                self.following = False
            else:
                instruction = ""

        return instruction