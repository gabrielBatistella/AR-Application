using System.IO;
using System.Net;
using System.Net.Sockets;

public class TCPConnector : Connector
{
    private TcpClient tcp = new TcpClient();
    private NetworkStream networkStream;

    public override void OpenCommunication(string ip, int port)
    {
        IPEndPoint serverEndpoint = new IPEndPoint(IPAddress.Parse(ip), port);

        tcp.Connect(serverEndpoint);
        networkStream = tcp.GetStream();
    }

    public override void CloseCommunication()
    {
        if (tcp.Connected)
        {
            networkStream.Dispose();
            tcp.Close();
        }
    }

    public override void SendData(byte[] data)
    {
        byte[] header = Int2Bytes(data.Length);

        networkStream.Write(header, 0, header.Length);
        networkStream.Write(data, 0, data.Length);
    }

    public override byte[] ReceiveResponse()
    {
        byte[] header = ReadAll(HeaderSize);
        int responseSize = Bytes2Int(header);

        byte[] responseData = ReadAll(responseSize);
        return responseData;
    }

    private byte[] ReadAll(int amountToRead)
    {
        byte[] readBuffer = new byte[amountToRead];

        int amountRead = 0;
        while (amountRead < amountToRead)
        {
            int bytesRead = networkStream.Read(readBuffer, amountRead, amountToRead - amountRead);
            if (bytesRead == 0)
            {
                throw new EndOfStreamException();
            }
            amountRead += bytesRead;
        }

        return readBuffer;
    }
}
