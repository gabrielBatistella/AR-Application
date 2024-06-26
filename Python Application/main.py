from Connection.server import Server
from Connection.tcpConnector import TCPConnector
from Connection.udpConnector import UDPConnector
from vcranium import VCranium
from Camera.photor import Photor
from Tests.detecVar import DetecVar
from Tests.betaVar import BetaVar

def main():
    server = Server(TCPConnector, VCranium)
    server.run()

if __name__ == '__main__' : main()