import time
import traceback
from threading import Thread

class CommunicationCloseException(Exception):
    def __init__(self):
        super().__init__('Client request to close environment.')

class Server():

    def __init__(self, Connector, Handler):
        self._Connector = Connector
        self._Handler = Handler

        self._com = None
        self._env = None

        self._managerThread = Thread(target=self._manageClients, args=())
        self._managerThread.daemon = True

    def run(self):
        self.start()
        try:
            while self.isRunning(): time.sleep(10)
        except KeyboardInterrupt:
            print('Server execution interrupted.')
        except:
            print('An error ocurred => ' + traceback.format_exc())
        finally:
            self.close()

    def start(self):
        self._com = self._Connector()
        self._managerThread.start()

    def close(self):
        print('Closing server devices...')
        del self._com
        print('Server down.')

    def isRunning(self):
        return self._managerThread.is_alive()



    def _manageClients(self):
        while True:
            print('Waiting for client...')
            self._com.openCommunication(*(self._com.waitForClient()))
            self._env = self._Handler()

            print('Running environment...')
            self._runEnvironment()

            print('Closing environment...')
            self._com.closeCommunication()
            del self._env

            print()

    def _runEnvironment(self):
        try:
            t = time.time()
            while True:          
                data, dataSize = self._com.receiveData()
                output = self._env.operateOnData(data)

                deltaT = time.time() - t
                connectionInfo = f'{round(1/deltaT)} FPS{self._Handler.inHeaderInfoSeparator}{round((dataSize/1024**2)/deltaT, 2)} MBps' if deltaT > 0 else f'0 FPS{self._Handler.inHeaderInfoSeparator}0.00 MBps'
                t = time.time()

                response = connectionInfo + self._Handler.headerBodySeparator + output
                self._com.sendResponse(response)

        except (CommunicationCloseException, OSError):
            return