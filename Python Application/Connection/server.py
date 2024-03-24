import time
import traceback
import abc

class EnvironmentCloseException(Exception):
    def __init__(self):
        super().__init__('Client request to close environment.')



class Server(abc.ABC):

    def __init__(self, socket):
        self._mainSocket = socket

    def run(self):
        try:
            self._watchClients()
        except KeyboardInterrupt:
            print('Server execution interrupted.')
        except:
            print('An error ocurred => ' + traceback.format_exc())
        finally:
            print('Closing server devices...')
            self._mainSocket.close()
            print('Server down.')



    @abc.abstractmethod
    def _waitForClient(self):
        pass

    @abc.abstractmethod
    def _createEnvironment(self, conn, addr):
        pass

    @abc.abstractmethod
    def _destroyEnvironment(self):
        pass

    @abc.abstractmethod
    def _receiveData(self):
        pass

    @abc.abstractmethod
    def _sendResponse(self, response):
        pass



    def _watchClients(self):
        while True:
            print('Waiting for client...')
            handler = self._createEnvironment(*(self._waitForClient()))

            print(f'Running environment...')
            self._runEnvironment(handler)

            print(f'Closing environment...')
            self._destroyEnvironment()

            print()

    def _runEnvironment(self, handler):
        try:
            t = time.time()
            while True:          
                data, dataSize = self._receiveData()
                output = handler.operateOnData(data)

                deltaT = time.time() - t
                connectionInfo = f'{round(1/deltaT)} FPS{handler.__class__.inHeaderInfoSeparator}{round((dataSize/1024**2)/deltaT, 2)} MBps' if deltaT > 0 else f'0 FPS{handler.__class__.inHeaderInfoSeparator}0.00 MBps'
                t = time.time()

                response = connectionInfo + handler.__class__.headerBodySeparator + output
                self._sendResponse(response)

        except (EnvironmentCloseException, OSError):
            return