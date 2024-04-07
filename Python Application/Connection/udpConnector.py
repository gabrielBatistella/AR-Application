import socket
from Connection.connector import Connector
from Connection.server import CommunicationCloseException

class UDPConnector(Connector):

    headerSize = 8
    frameBufferSize = 128

    def __init__(self, ip = socket.gethostbyname(socket.gethostname()), port = 5052):
        super().__init__()
        print('Server type: UDP')
        
        self._conn = UDPConnector._initSocket(ip, port)
        print(f'Host IP: {ip} | Port: {port}')

        self._addr = None

        self._frameBuffer = [None] * UDPConnector.frameBufferSize
        self._frameSeq = [None] * UDPConnector.frameBufferSize

    def __del__(self):
        super().__del__()

        self.closeCommunication()
        self._conn.close()



    def waitCommunication(self):
        if self._addr is None:
            addr = UDPConnector._waitConnection(self._conn)

            print(f'Connection accepted with client {addr}.')
            self._addr = addr
        else:
            print(f'Already connected to {self._addr}.')

    def closeCommunication(self):
        if self._addr is not None:
            UDPConnector._closeConnection()

            print(f'Connection with client {self._addr} closed.')
            self._addr = None
        else:
            print('Not connected to any client.')

    def receiveData(self):
        if self._addr is not None:
            while True:
                fragment = UDPConnector._recvonlyfrom(self._conn, self._addr)
                frameCount, numFragments, currentFragment, fragmentSize, fragmentData = UDPConnector._parseFragment(fragment)

                frameIndex = frameCount % UDPConnector.frameBufferSize

                if self._frameSeq[frameIndex] != frameCount:
                    
                    if self._frameBuffer[frameIndex] is not None: print("Pacote perdido!")

                    self._frameBuffer[frameIndex] = [None] * numFragments
                    self._frameSeq[frameIndex] = frameCount
                    
                self._frameBuffer[frameIndex][currentFragment] = fragmentData

                if not any(fragment is None for fragment in self._frameBuffer[frameIndex]):
                    data = b''.join(self._frameBuffer[frameIndex])

                    self._frameBuffer[frameIndex] = None
                    self._frameSeq[frameIndex] = None
                    
                    return data, len(data)
        else:
            raise ValueError()

    def sendResponse(self, responseInfo):
        if self._addr is not None:
            response = responseInfo.encode('utf-8')
            self._conn.sendto(response, self._addr)
        else:
            raise ValueError()



    @staticmethod
    def _initSocket(ip, port):      
        newSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        newSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        newSocket.bind((ip, port))
        newSocket.settimeout(None)
        return newSocket

    @staticmethod
    def _waitConnection(listenerSocket):
        while True:
            try:
                test, addr = listenerSocket.recvfrom(65535)
                listenerSocket.sendto(test, addr)
                return addr
            except ConnectionResetError: 
                continue

    @staticmethod
    def _closeConnection():
        pass

    @staticmethod
    def _recvonlyfrom(conn, addr):
        senderAddr = None
        while senderAddr != addr:
            try:
                conn.settimeout(5.0)
                data, senderAddr = conn.recvfrom(65535)
            except (TimeoutError, ConnectionResetError):
                raise CommunicationCloseException()
            finally:
                conn.settimeout(None)
        return data
    
    @staticmethod
    def _parseFragment(fragment):
        fragmentHeader, fragmentData = fragment[:UDPConnector.headerSize], fragment[UDPConnector.headerSize:]
        frameCount = int.from_bytes(fragmentHeader[:2], 'big')
        numFragments = int.from_bytes(fragmentHeader[2:4], 'big')
        currentFragment = int.from_bytes(fragmentHeader[4:6], 'big')
        fragmentSize = int.from_bytes(fragmentHeader[6:], 'big')
        return frameCount, numFragments, currentFragment, fragmentSize, fragmentData