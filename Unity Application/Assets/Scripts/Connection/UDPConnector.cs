using System.IO;
using System.Net;
using System.Net.Sockets;

public class UDPConnector : Connector
{
    private UdpClient udp = new UdpClient();

    public override void OpenCommunication(string ip, int port)
    {
        IPEndPoint serverEndpoint = new IPEndPoint(IPAddress.Parse(ip), port);

        udp.Connect(serverEndpoint);
        TestServerListening();
    }

    public override void CloseCommunication()
    {
        udp.Close();
    }

    public override void SendData(byte[] data)
    {
        udp.Send(data, data.Length);
    }

    public override byte[] ReceiveResponse()
    {
        try
        {
            udp.Client.ReceiveTimeout = 5000;

            IPEndPoint remoteEndpoint = new IPEndPoint(IPAddress.Any, 0);
            byte[] responseData = udp.Receive(ref remoteEndpoint);
            return responseData;
        }
        catch (SocketException)
        {
            throw new EndOfStreamException();
        }
        finally
        {
            udp.Client.ReceiveTimeout = 0;
        }
    }

    private void TestServerListening()
    {
        udp.Send(new byte[HeaderSize], HeaderSize);

        try
        {
            udp.Client.ReceiveTimeout = 2000;

            IPEndPoint remoteEndpoint = new IPEndPoint(IPAddress.Any, 0);
            udp.Receive(ref remoteEndpoint);
        }
        catch (SocketException)
        {
            throw;
        }
        finally
        {
            udp.Client.ReceiveTimeout = 0;
        }
    }
}
