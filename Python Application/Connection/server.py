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

        self._communication = None
        self._environment = None

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
        self._communication = self._Connector()
        self._managerThread.start()

    def close(self):
        print('Closing server devices...')
        del self._communication
        print('Server down.')

    def isRunning(self):
        return self._managerThread.is_alive()



    def _manageClients(self):
        while True:
            print('Waiting for client...')
            self._communication.waitCommunication()
            self._environment = self._Handler()

            print('Running environment...')
            self._runEnvironment()

            print('Closing environment...')
            self._communication.closeCommunication()
            del self._environment

            print()

    def _runEnvironment(self):
        try:
            t = time.time()
            while True:          
                data, dataSize = self._communication.receiveData()
                output = self._environment.operateOnData(data)

                deltaT = time.time() - t
                connectionInfo = f'{round(1/deltaT)} FPS{self._Handler.inDetailsInfoSeparator}{round((dataSize/1024**2)/deltaT, 2)} MBps' if deltaT > 0 else f'0 FPS{self._Handler.inDetailsInfoSeparator}0.00 MBps'
                t = time.time()

                response = connectionInfo + self._Handler.detailsBodySeparator + output
                self._communication.sendResponse(response)

        except CommunicationCloseException:
            return
        
        except:
            print('An error ocurred => ' + traceback.format_exc())