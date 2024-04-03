import abc

class Connector(abc.ABC):

    def __init__(self):
        pass

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
    def sendResponse(self, response):
        pass