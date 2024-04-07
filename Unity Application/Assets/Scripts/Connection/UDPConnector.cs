using System.IO;
using System.Linq;
using System.Net;
using System.Net.Sockets;
using System.Text;
using UnityEngine;

public class UDPConnector : Connector
{
    [SerializeField] private int maxFragmentSize = 512;
    [SerializeField] private int maxFrameSeq = 512;

    private UdpClient udp = new UdpClient();
    private int framesSentCount;

    public override void OpenCommunication(string ip, int port)
    {
        IPEndPoint serverEndpoint = new IPEndPoint(IPAddress.Parse(ip), port);

        udp.Connect(serverEndpoint);
        TestServerListening();

        framesSentCount = 0;
    }

    public override void CloseCommunication()
    {
        udp.Close();
    }

    public override void SendData(byte[] data)
    {
        byte[][] fragmentedData = FragmentFrameData(data, framesSentCount);

        foreach (byte[] fragment in fragmentedData)
        {
            udp.Send(fragment, fragment.Length);
        }

        framesSentCount = (framesSentCount + 1) % maxFrameSeq;
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
        byte[] message = Encoding.UTF8.GetBytes("SYN");
        udp.Send(message, message.Length);

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

    private byte[][] FragmentFrameData(byte[] data, int currentFrameCount)
    {
        byte[] frameCountHeader = Short2Bytes((short) currentFrameCount);

        int fragmentSize = maxFragmentSize - HeaderSize;
        int numFragments = Mathf.CeilToInt((float) data.Length / fragmentSize);
        byte[] numFragmentsHeader = Short2Bytes((short) numFragments);

        byte[] headerFrame = frameCountHeader.Concat(numFragmentsHeader).ToArray();

        byte[][] fragmentedData = new byte[numFragments][];
        int currentFragment = 0;

        while (currentFragment < numFragments)
        {
            byte[] currentFragmentHeader = Short2Bytes((short) currentFragment);

            int currentFragmentSize = currentFragment == numFragments - 1 ? data.Length - currentFragment * fragmentSize : fragmentSize;
            byte[] currentFragmentSizeHeader = Short2Bytes((short) currentFragmentSize);

            byte[] headerFragment = headerFrame.Concat(currentFragmentHeader).Concat(currentFragmentSizeHeader).ToArray();

            int startIndex = currentFragment * fragmentSize;
            int finalIndex = startIndex + currentFragmentSize;

            fragmentedData[currentFragment] = headerFragment.Concat(data[startIndex..finalIndex]).ToArray();
            currentFragment++;
        }

        return fragmentedData;
    }
}
