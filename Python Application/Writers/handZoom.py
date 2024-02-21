from Writers.instructionWriter import InstructionWriter
import math

class HandZoom(InstructionWriter):
    
    def __init__(self, inInstructionHandleValueSeparator):
        super().__init__(inInstructionHandleValueSeparator)

        self.menu = 0
        self.loading = False
        self.delay = 0
        self.mode = 0
        self.modeCurrent = 0

    def generateInstruction(self, detector, trackObjs, camCalib):
        instruction = "Menu" + self.inInstructionHandleValueSeparator

        if len(trackObjs) == 2:
            hand1 = trackObjs[0]
            hand2 = trackObjs[1]