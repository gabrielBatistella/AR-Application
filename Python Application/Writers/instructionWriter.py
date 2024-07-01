import abc

class InstructionWriter(abc.ABC):
   
    beta = 1 - 1/3
    
    def __init__(self, inInstructionHandleValueSeparator, modeMask):
        self.inInstructionHandleValueSeparator = inInstructionHandleValueSeparator
        self.modeMask = int('{:06b}'.format(modeMask)[::-1], 2)

    @abc.abstractmethod
    def generateInstruction(self, detector, trackObjs, camCalib):
        pass

    def shouldExecuteInMode(self, mode):
        return self.modeMask & 2**mode > 0
    
    @staticmethod
    def filterPointEWA(realPoint, previousFilteredPoint):
        return [previousFilteredPoint[i]*InstructionWriter.beta + realPoint[i]*(1-InstructionWriter.beta) for i in range(3)]
