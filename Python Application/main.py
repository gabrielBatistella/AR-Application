from Connection.server import Server
from Connection.tcpConnector import TCPConnector
from Connection.udpConnector import UDPConnector
from vcranium import VCranium
from Camera.photor import Photor

def main():
    server = Server(UDPConnector, VCranium)
    server.run()

if __name__ == '__main__' : main()