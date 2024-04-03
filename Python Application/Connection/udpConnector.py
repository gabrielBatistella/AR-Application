import socket
from Connection.connector import Connector
from Connection.server import CommunicationCloseException

class UDPConnector(Connector):

    def __init__(self, ip = socket.gethostbyname(socket.gethostname()), port = 5050):
        super().__init__()
        print('Server type: UDP')
        
        self._conn = UDPConnector._initSocket(ip, port)
        print(f'Host IP: {ip} | Port: {port}')

        self._addr = None

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
            dataBytes = UDPConnector._recvonlyfrom(self._conn, self._addr)
            return dataBytes, len(dataBytes)
        else:
            raise ValueError()

    def sendResponse(self, response):
        if self._addr is not None: 
            infoEncoded = response.encode('utf-8')
            self._conn.sendto(infoEncoded, self._addr)
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
        _, senderAddr = listenerSocket.recvfrom(65535)
        return senderAddr

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
            except:
                raise CommunicationCloseException()
            finally:
                conn.settimeout(None)
        return data