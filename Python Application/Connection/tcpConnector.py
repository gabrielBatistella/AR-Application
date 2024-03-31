import socket
from Connection.connector import Connector
from Connection.server import CommunicationCloseException

class TCPConnector(Connector):

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



    def waitForClient(self):
        self._listenerSocket.listen(1)
        conn, addr = self._listenerSocket.accept()
        return conn, addr

    def openCommunication(self, conn, addr):
        if self._conn is None:
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
            readBuffer_header = TCPConnector._recvall(self._conn, 16)
            header = readBuffer_header.decode('utf-8')
            dataSize = int(header)

            readBuffer_data = TCPConnector._recvall(self._conn, dataSize)

            return readBuffer_data, dataSize
        else:
            raise ValueError()

    def sendResponse(self, response):
        if self._conn is not None: 
            headerEncoded = str(len(response)).ljust(16).encode('utf-8')
            infoEncoded = response.encode('utf-8')
        
            self._conn.sendall(headerEncoded)
            self._conn.sendall(infoEncoded)
        else:
            raise ValueError()



    @staticmethod
    def _initSocket(ip, port):      
        newSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        newSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)      
        newSocket.bind((ip, port))
        #newSocket.settimeout(1.0)
        #newSocket.setblocking(0)
        return newSocket
    
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