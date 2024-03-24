import socket
from server import Server, EnvironmentCloseException



class TCPServer(Server):

    def __init__(self, handlerClass, ip = socket.gethostbyname(socket.gethostname()), port = 5050):
        print('Server type: TCP')
        super().__init__(TCPServer._initSocket(ip, port))

        self._handlerClass = handlerClass

        self._conn = None
        self._addr = None



    def _createEnvironment(self):
        self._listenerSock.listen(1)
        conn, addr = self._listenerSock.accept()
        print(f'Connection accepted with client {addr}.')

        self._conn = conn
        self._addr = addr

        return self._handlerClass()

    def _destroyEnvironment(self):
        TCPServer._closeConnection(self._conn, self._addr)

        self._conn = None
        self._addr = None

    def _receiveData(self):
        readBuffer_header = TCPServer._recvall(self._conn, 16)
        header = readBuffer_header.decode('utf-8')
        dataSize = int(header)

        readBuffer_data = TCPServer._recvall(self._conn, dataSize)

        return readBuffer_data, dataSize

    def _sendResponse(self, response):
        headerEncoded = str(len(response)).ljust(16).encode('utf-8')
        infoEncoded = response.encode('utf-8')
    
        self._conn.sendall(headerEncoded)
        self._conn.sendall(infoEncoded)



    @staticmethod
    def _initSocket(ip, port):      
        print(f'Host IP: {ip} | Port: {port}')

        newSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        newSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)      
        newSocket.bind((ip, port))
        # newSocket.settimeout(1.0)
        # newSocket.setblocking(0)

        return newSocket
    
    @staticmethod
    def _closeConnection(conn, addr):
        conn.shutdown(socket.SHUT_RDWR)
        conn.close()
        print(f'Connection with client {addr} closed')
    
    @staticmethod
    def _recvall(conn, amount):
        buf = b''
        while amount:
            newbuf = conn.recv(amount)
            if len(newbuf) == 0:
                raise EnvironmentCloseException()
            buf += newbuf
            amount -= len(newbuf)
        return buf