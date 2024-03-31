from Connection.server import Server
from Connection.tcpConnector import TCPConnector
from vcranium import VCranium

def main():
    server = Server(TCPConnector, VCranium)
    server.run()

if __name__ == '__main__' : main()