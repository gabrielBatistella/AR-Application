import abc

class Handler(abc.ABC):

    def __init__(self):
        pass

    def __del__(self):
        pass

    @abc.abstractmethod
    def operateOnData(self, data):
        pass