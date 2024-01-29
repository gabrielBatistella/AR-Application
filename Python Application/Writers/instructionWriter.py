import abc

class InstructionWriter(abc.ABC):

    def __init__(self, inInstructionHandleValueSeparator):
        self.inInstructionHandleValueSeparator = inInstructionHandleValueSeparator

    @abc.abstractmethod
    def generateInstruction(self, detector, trackObjs, camCalib):
        pass