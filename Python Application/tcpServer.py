import socket
import select
import time
import traceback
from threading import Thread
from multiprocessing import Process
import abc

class ConnectionCloseException(Exception):
    pass

class TCPServer(abc.ABC):

    def __init__(self, ip, port):
        self.listenerSock = self._initSocket(ip, port)
        self.conns = None
        self.addrs = None

    @abc.abstractmethod
    def operateOnDataReceived(self, data):
        pass

    def start(self): #cria thread para handleListening e fica em while {}
        pass
       
    def _initSocket(self, ip, port):      
        print(f"Host IP: {ip} | Port: {port}")

        newSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        newSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)      
        newSock.bind((ip, port))
        # newSock.settimeout(1.0)
        # newSock.setblocking(0)

        return newSock
    
    def _isConnected(self, conn):
        try:
            conn.sendall("some data")
            return True
        except:
            return False

    def _recvall(self, conn, amount):
        buf = b''
        while amount:
            newbuf = conn.recv(amount)
            if newbuf == "":
                raise ConnectionCloseException("Client request to close connection. Closing...")
            buf += newbuf
            amount -= len(newbuf)
        return buf
    
    def _receiveData(self, conn):
        readBuffer_header = self._recvall(conn, 16)
        header = readBuffer_header.decode("utf-8")
        dataSize = int(header)

        readBuffer_data = self._recvall(conn, dataSize)

        return readBuffer_data, dataSize
    
    def _handleConnection(self, conn, addr):
        connectionInfo = ""
        frame_counter, buffer_counter = 0, 0
        t = time.time()

        try:
            while True:            
                data, dataSize = self._receiveData(conn)

                output = self.operateOnDataReceived(data)

                infoToSend = connectionInfo + ":" + output

                headerEncoded = str(len(infoToSend)).ljust(16).encode('utf-8')
                infoEncoded = infoToSend.encode('utf-8')
            
                conn.sendall(headerEncoded)
                conn.sendall(infoEncoded)

                frame_counter += 1
                buffer_counter += dataSize

                if time.time() - t > 1:
                    connectionInfo = str(frame_counter) + "~" + str(round(buffer_counter/1024**2, 2))
                    frame_counter, buffer_counter = 0, 0
                    t = time.time()

        except ConnectionCloseException:
            if self._isConnected(conn):
                conn.shutdown(socket.SHUT_RDWR)
                conn.close()
            raise ConnectionCloseException(f'Connection with address {addr} closed')

        except Exception:
            if self._isConnected(conn):
                conn.shutdown(socket.SHUT_RDWR)
                conn.close()
            raise Exception(f'An error ocurred in the connection with {addr} => ' + traceback.format_exc())
        
    def _handleListening(self):
        processes = []
        try:
            while True:
                print(f"Socket mode: {self.listenerSock.getblocking()}")
                print(f"Timeout time: {self.listenerSock.timeout}")

                while True:
                    print('Waiting for connection.')
                    self.listenerSock.listen(1)
                    # Sockets from which we expect to read
                    inputs = [self.listenerSock]
                    readable, _, _ = select.select(inputs, inputs, inputs)
                    # Sockets to which we expect to write
                    if readable:
                        conn = readable[0]
                        break
                    else: 
                        continue
                
                conn, addr = self.listenerSock.accept()
                print(f'Connection accepted with device {addr}.')
                
                p = Process(target=self._handleConnection, args=(conn, addr))
                processes.append(p)
                # p.daemon = True
                p.start()
                p.join()

        except ConnectionCloseException as error:
            print(error)
            
        except Exception:
            print()
            print(traceback.format_exc())
            print('Closing all server and connected devices.')

            for p in processes:
                p.join()
                p.terminate()
                
            self.listenerSock.close()