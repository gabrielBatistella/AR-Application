import time
import traceback

class CommunicationCloseException(Exception):
    def __init__(self):
        super().__init__('Client request to close environment.')

class Server():

    def __init__(self, Connector, Handler):
        self._Connector = Connector
        self._Handler = Handler

    def run(self):
        try:
            connector = self._Connector()
            self._manageClients(connector)
        except KeyboardInterrupt:
            print('Server execution interrupted.')
        except:
            print('An error ocurred => ' + traceback.format_exc())
        finally:
            print('Closing server devices...')
            del connector
            print('Server down.')



    def _manageClients(self, connector):
        while True:
            print('Waiting for client...')
            connector.openCommunication(*(connector.waitForClient()))
            handler = self._Handler()

            print('Running environment...')
            self._runEnvironment(connector, handler)

            print('Closing environment...')
            connector.closeCommunication()
            del handler

            print()

    def _runEnvironment(self, connector, handler):
        try:
            t = time.time()
            while True:          
                data, dataSize = connector.receiveData()
                output = handler.operateOnData(data)

                deltaT = time.time() - t
                connectionInfo = f'{round(1/deltaT)} FPS{handler.__class__.inHeaderInfoSeparator}{round((dataSize/1024**2)/deltaT, 2)} MBps' if deltaT > 0 else f'0 FPS{handler.__class__.inHeaderInfoSeparator}0.00 MBps'
                t = time.time()

                response = connectionInfo + handler.__class__.headerBodySeparator + output
                connector.sendResponse(response)

        except (CommunicationCloseException, OSError):
            return