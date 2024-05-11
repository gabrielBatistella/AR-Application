import abc

class Connector(abc.ABC):

    @property
    @abc.abstractmethod
    def protocol(self):
        pass

    def __init__(self):
        print(f'Server type: {self.__class__.protocol}')

    def __del__(self):
        pass

    @abc.abstractmethod
    def waitCommunication(self):
        pass

    @abc.abstractmethod
    def closeCommunication(self):
        pass

    @abc.abstractmethod
    def receiveData(self):
        pass

    @abc.abstractmethod
    def sendResponse(self, responseInfo):
        pass