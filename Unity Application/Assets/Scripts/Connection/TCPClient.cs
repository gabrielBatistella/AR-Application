using System;
using System.IO;
using System.Net;
using System.Net.Sockets;
using System.Text;
using UnityEngine;
using System.Collections;
using System.Threading;
using UnityEngine.UI;

public abstract class TCPClient : MonoBehaviour
{
    [Header("Server Connection")]
    [SerializeField] private string defaultServerIP;
    [SerializeField] private int defaultServerPort;

    [SerializeField] private bool startConnecting;

    [Header("UI for Connection Info")]
    [SerializeField] private Text connTextField;

    [Header("Encoding Details")]
    [SerializeField] private int headerSize;

    private Socket socket;
    private NetworkStream networkStream;

    private CommunicationSynchron syncObj;

    private bool connected = false;
    public bool Connected { get => connected; }

    protected string specificConnectionInfo = "";

    private class CommunicationSynchron
    {
        public byte[] recvData = null;
        public bool recvFlag = false;
        public int recvBalance = 0;

        public bool comDown = false;
    }

    protected virtual void Start()
    {
        if (startConnecting)
        {
            TryToConnect();
        }
    }

    public bool TryToConnect()
    {
        return TryToConnect(defaultServerIP, defaultServerPort);
    }

    public bool TryToConnect(string ip, int port)
    {
        if (socket != null && socket.Connected)
        {
            Debug.Log("Already connected to a server");

            connected = false;
            return false;
        }

        Debug.Log("Connecting to " + ip + "...");
        try
        {
            ConnectSocket(ip, port);
            Debug.Log("Connected: " + ip);

            syncObj = new CommunicationSynchron();
            StartCoroutine(ReceivingRoutine());

            connected = true;
            return true;
        }
        catch (SocketException)
        {
            Debug.Log("Connection refused!\n");

            connected = false;
            return false;
        }
        catch (Exception e)
        {
            Debug.Log("Fatal error while connecting to server! - " + e + "\n");

            connected = false;
            return false;
        }
    }

    private void OnDestroy()
    {
        CloseSocket();
        connected = false;
    }

    protected virtual void StopClient()
    {
        Debug.Log("Stopping client...");

        CloseSocket();
        connected = false;
    }

    protected void SendToServer(byte[] data)
    {
        string header = data.Length.ToString().PadRight(headerSize);
        byte[] headerEncoded = Encoding.UTF8.GetBytes(header);

        networkStream.Write(headerEncoded, 0, headerSize);
        networkStream.Write(data, 0, data.Length);

        lock (syncObj)
        {
            syncObj.recvBalance--;
            connTextField.text = specificConnectionInfo + "Balance: " + syncObj.recvBalance;
        }
    }

    protected abstract void UseDataReceivedFromServer(byte[] data);

    private IEnumerator ReceivingRoutine()
    {
        Thread receivingThread = new Thread(ReceivingFromServer);
        receivingThread.Start();

        while (true)
        {
            lock (syncObj)
            {
                if (syncObj.comDown)
                {
                    StopClient();
                    yield break;
                }
                else if (syncObj.recvFlag)
                {
                    UseDataReceivedFromServer(syncObj.recvData);
                    syncObj.recvFlag = false;
                }
            }
            yield return null;
        }
    }

    private void ReceivingFromServer()
    {
        try
        {
            while (true)
            {
                byte[] readBuffer_header = ReadAll(networkStream, headerSize);
                string header = Encoding.UTF8.GetString(readBuffer_header, 0, headerSize);
                int dataSize = int.Parse(header);

                byte[] readBuffer_data = ReadAll(networkStream, dataSize);

                lock (syncObj)
                {
                    syncObj.recvData = readBuffer_data;
                    syncObj.recvFlag = true;
                    syncObj.recvBalance++;
                }
            }
        }
        catch (EndOfStreamException)
        {
            Debug.Log("Connection closed!\n");
            lock (syncObj)
            {
                syncObj.comDown = true;
            }
        }
        catch (Exception e)
        {
            Debug.Log("Error receiving data! - " + e + "\n");
            lock (syncObj)
            {
                syncObj.comDown = true;
            }
        }
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

    private void ConnectSocket(string ip, int port)
    {
        IPEndPoint endpoint = new IPEndPoint(IPAddress.Parse(ip), port);
        socket = new Socket(endpoint.AddressFamily, SocketType.Stream, ProtocolType.Tcp);
        socket.Connect(endpoint);
        networkStream = new NetworkStream(socket, true);
    }

    private void CloseSocket()
    {
        if (socket != null && socket.Connected)
        {
            try
            {
                socket.Shutdown(SocketShutdown.Both);
            }
            finally
            {
                networkStream.Dispose();
                socket.Close();
            }
        }
    }
}
