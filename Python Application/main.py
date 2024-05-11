from Connection.server import Server
from Connection.tcpConnector import TCPConnector
from Connection.udpConnector import UDPConnector
from vcranium import VCranium
from Camera.photor import Photor
from Tests.handlera import HandlerA
from Tests.handlerb import HandlerB
from Tests.handlerapnp import HandlerAPNP

def main():
    server = Server(TCPConnector, HandlerAPNP)
    server.run()

if __name__ == '__main__' : main()