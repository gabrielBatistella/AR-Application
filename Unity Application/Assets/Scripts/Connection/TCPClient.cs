using System.IO;
using System.Net;
using System.Net.Sockets;
using System.Text;
using UnityEngine;

public abstract class TCPClient : Client
{
    [Header("Encoding Details")]
    [SerializeField] private int headerSize;

    private TcpClient tcp = new TcpClient();
    private NetworkStream networkStream;

    protected override void OpenCommunication(string ip, int port)
    {
        IPEndPoint endpoint = new IPEndPoint(IPAddress.Parse(ip), port);

        tcp.Connect(endpoint);
        networkStream = tcp.GetStream();
    }

    protected override void CloseCommunication()
    {
        if (tcp.Connected)
        {
            networkStream.Dispose();
            tcp.Close();
        }
    }

    protected override void SendData(byte[] data)
    {
        string header = data.Length.ToString().PadRight(headerSize);
        byte[] headerEncoded = Encoding.UTF8.GetBytes(header);

        networkStream.Write(headerEncoded, 0, headerSize);
        networkStream.Write(data, 0, data.Length);
    }

    protected override byte[] ReceiveResponse()
    {
        byte[] headerData = ReadAll(networkStream, headerSize);
        string header = Encoding.UTF8.GetString(headerData, 0, headerSize);
        int responseSize = int.Parse(header);

        byte[] responseData = ReadAll(networkStream, responseSize);
        return responseData;
    }

    private byte[] ReadAll(NetworkStream networkStream, int amountToRead)
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
