using System.IO;
using System.Net;
using System.Net.Sockets;
using System.Text;
using UnityEngine;

public class TCPConnector : Connector
{
    private TcpClient tcp = new TcpClient();
    private NetworkStream networkStream;

    public override void OpenCommunication(string ip, int port)
    {
        IPEndPoint endpoint = new IPEndPoint(IPAddress.Parse(ip), port);

        tcp.Connect(endpoint);
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
        string header = data.Length.ToString().PadRight(HeaderSize);
        byte[] headerEncoded = Encoding.UTF8.GetBytes(header);

        networkStream.Write(headerEncoded, 0, HeaderSize);
        networkStream.Write(data, 0, data.Length);
    }

    public override byte[] ReceiveResponse()
    {
        byte[] headerData = ReadAll(HeaderSize);
        string header = Encoding.UTF8.GetString(headerData, 0, HeaderSize);
        int responseSize = int.Parse(header);

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
