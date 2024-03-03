import socket
import time
import traceback
from threading import Thread
import abc

class ConnectionCloseException(Exception):
    def __init__(self):
        super().__init__('Client request to close connection.')



class TCPServer(abc.ABC):

    def __init__(self, ip, port):
        self._listenerSock = TCPServer._initSocket(ip, port)
        self._listenerThread = Thread(target=self._handleListening, args=())
        self._listenerThread.daemon = True

        self._conns = []
        self._addrs = []
        self._handlers = []

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
        self._listenerThread.start()

    def close(self):
        print('Closing all server and connected devices...')

        self._listenerSock.close()

        while len(self._handlers) > 0:
            self._handlers.pop()

        while len(self._conns) > 0:
            conn, addr = self._conns.pop(), self._addrs.pop()
            if TCPServer._isConnected(conn):
                TCPServer._closeConnection(conn, addr)
            
        print('Server down.')

    def isRunning(self):
        return self._listenerThread.is_alive()



    @abc.abstractmethod
    def _operateOnDataReceived(self, data):
        pass
    
    def _handleConnection(self, conn, addr):
        t = time.time()
        try:
            while True:          
                data, dataSize = TCPServer._receiveData(conn)
                output = self._operateOnDataReceived(data)

                deltaT = time.time() - t
                connectionInfo = str(round(1/deltaT)) + ' FPS' + self.__class__.inHeaderInfoSeparator + str(round((dataSize/1024**2)/deltaT, 2)) + ' MBps' if deltaT > 0 else '0 FPS' + self.__class__.inHeaderInfoSeparator + '0.00 MBps'
                t = time.time()

                infoToSend = connectionInfo + self.__class__.headerBodySeparator + output

                headerEncoded = str(len(infoToSend)).ljust(16).encode('utf-8')
                infoEncoded = infoToSend.encode('utf-8')
            
                conn.sendall(headerEncoded)
                conn.sendall(infoEncoded)

        except ConnectionCloseException:
            TCPServer._closeConnection(conn, addr)

        except OSError:
            print(f'The connection with {addr} is closed')
            #TCPServer._closeConnection(conn, addr)

        except:
            print(f'An error ocurred in the connection with {addr} => ' + traceback.format_exc())
            TCPServer._closeConnection(conn, addr)
        
    def _handleListening(self):
        try:
            print(f'Socket mode: {self._listenerSock.getblocking()}')
            print(f'Timeout time: {self._listenerSock.timeout}')
            print('Waiting for connections...')

            while True:
                self._listenerSock.listen(1)
                conn, addr = self._listenerSock.accept()
                print(f'Connection accepted with device {addr}.')

                thr = Thread(target=self._handleConnection, args=(conn, addr))
                thr.daemon = True
                thr.start()

                self._conns.append(conn)
                self._addrs.append(addr)
                self._handlers.append(thr)
            
        except OSError:
            print('Stopped listening.')

        except:
            print(traceback.format_exc())



    @staticmethod
    def _initSocket(ip, port):      
        print(f'Host IP: {ip} | Port: {port}')

        newSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        newSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)      
        newSock.bind((ip, port))
        # newSock.settimeout(1.0)
        # newSock.setblocking(0)

        return newSock
    
    @staticmethod
    def _closeConnection(conn, addr):
        try:
            conn.shutdown(socket.SHUT_RDWR)
            conn.close()
            print(f'Connection with client {addr} closed')
        except OSError:
            print(f'Connection with client {addr} was already closed')
        except:
            print(traceback.format_exc())

    @staticmethod
    def _isConnected(conn):
        try:
            conn.sendall(b'')
            return True
        except:
            return False

    @staticmethod
    def _recvall(conn, amount):
        buf = b''
        while amount:
            newbuf = conn.recv(amount)
            if len(newbuf) == 0:
                raise ConnectionCloseException()
            buf += newbuf
            amount -= len(newbuf)
        return buf
    
    @staticmethod
    def _receiveData(conn):
        readBuffer_header = TCPServer._recvall(conn, 16)
        header = readBuffer_header.decode('utf-8')
        dataSize = int(header)

        readBuffer_data = TCPServer._recvall(conn, dataSize)

        return readBuffer_data, dataSize