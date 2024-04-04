from Connection.server import Server
from Connection.udpConnector import UDPConnector
from vcranium import VCranium

def main():
    server = Server(UDPConnector, VCranium)
    server.run()

if __name__ == '__main__' : main()