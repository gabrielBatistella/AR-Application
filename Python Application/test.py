import time
import traceback
import socket
from tcpServer import TCPServer

class VCraniumServer(TCPServer):
    def __init__(self, ip, port):
        super().__init__(ip, port)

    @classmethod
    def _operateOnDataReceived(self, data):
        return data.decode('utf-8')

def main():
    HOSTNAME = socket.gethostname()
    HOST = socket.gethostbyname(HOSTNAME)

    server = VCraniumServer(HOST, 5050)
    server.run()

if __name__ == '__main__' : main()