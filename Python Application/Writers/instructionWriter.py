import abc

class InstructionWriter(abc.ABC):

    def __init__(self, inInstructionHandleValueSeparator, modeMask):
        self.inInstructionHandleValueSeparator = inInstructionHandleValueSeparator
        self.modeMask = int('{:04b}'.format(modeMask)[::-1], 2)

    @abc.abstractmethod
    def getDisableInstruction(self):
        pass

    @abc.abstractmethod
    def generateInstruction(self, detector, trackObjs, camCalib):
        pass

    def shouldExecuteInMode(self, mode):
        return self.modeMask & 2**mode > 0