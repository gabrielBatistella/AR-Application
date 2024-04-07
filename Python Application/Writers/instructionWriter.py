import abc

class InstructionWriter(abc.ABC):
   
    beta = 0.90
    
    def __init__(self, inInstructionHandleValueSeparator, modeMask):
        self.inInstructionHandleValueSeparator = inInstructionHandleValueSeparator
        self.modeMask = modeMask

    @abc.abstractmethod
    def generateInstruction(self, detector, trackObjs, camCalib):
        pass

    def shouldExecuteInMode(self, mode):
        return self.modeMask & 2**(3-mode) > 0
    
    @staticmethod
    def filterPointEWA(realPoint, previousFilteredPoint):
        return (realPoint[i]*InstructionWriter.beta + previousFilteredPoint[i]*(1-InstructionWriter.beta) for i in range(3))