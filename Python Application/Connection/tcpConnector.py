import socket
from Connection.connector import Connector
from Connection.server import CommunicationCloseException

class TCPConnector(Connector):

    headerSize = 4

    def __init__(self, ip = socket.gethostbyname(socket.gethostname()), port = 5050):
        super().__init__()
        print('Server type: TCP')
        
        self._listenerSocket = TCPConnector._initSocket(ip, port)
        print(f'Host IP: {ip} | Port: {port}')

        self._conn = None
        self._addr = None

    def __del__(self):
        super().__del__()

        self.closeCommunication()
        self._listenerSocket.close()



    def waitCommunication(self):
        if self._conn is None:
            conn, addr = TCPConnector._waitConnection(self._listenerSocket)

            print(f'Connection accepted with client {addr}.')
            self._conn = conn
            self._addr = addr
        else:
            print(f'Already connected to {self._addr}.')

    def closeCommunication(self):
        if self._conn is not None:
            TCPConnector._closeConnection(self._conn)

            print(f'Connection with client {self._addr} closed.')
            self._conn = None
            self._addr = None
        else:
            print('Not connected to any client.')

    def receiveData(self):
        if self._conn is not None:
            header = TCPConnector._recvall(self._conn, TCPConnector.headerSize)
            dataSize = int.from_bytes(header, 'big')

            data = TCPConnector._recvall(self._conn, dataSize)
            return data, len(data)
        else:
            raise ValueError()

    def sendResponse(self, responseInfo):
        if self._conn is not None: 
            header = len(responseInfo).to_bytes(TCPConnector.headerSize, 'big')
            response = responseInfo.encode('utf-8')

            try:
                self._conn.sendall(header)
                self._conn.sendall(response)
            except ConnectionAbortedError:
                raise CommunicationCloseException()
        else:
            raise ValueError()



    @staticmethod
    def _initSocket(ip, port):      
        newSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        newSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        newSocket.bind((ip, port))
        newSocket.settimeout(None)
        return newSocket

    @staticmethod
    def _waitConnection(listenerSocket):
        listenerSocket.listen(1)
        conn, addr = listenerSocket.accept()
        return conn, addr

    @staticmethod
    def _closeConnection(conn):
        conn.shutdown(socket.SHUT_RDWR)
        conn.close()

    @staticmethod
    def _recvall(conn, amount):
        buf = b''
        while amount:
            newbuf = conn.recv(amount)
            if len(newbuf) == 0:
                raise CommunicationCloseException()
            buf += newbuf
            amount -= len(newbuf)
        return buf