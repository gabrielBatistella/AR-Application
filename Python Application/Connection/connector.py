import abc

class Connector(abc.ABC):

    def __init__(self):
        pass

    def __del__(self):
        pass

    @abc.abstractmethod
    def waitForClient(self):
        pass

    @abc.abstractmethod
    def openCommunication(self, conn, addr):
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