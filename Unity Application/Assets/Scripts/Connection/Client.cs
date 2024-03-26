using System;
using System.IO;
using System.Net.Sockets;
using UnityEngine;
using System.Collections;
using System.Threading;
using UnityEngine.UI;

public abstract class Client : MonoBehaviour
{
    [Header("Server Info")]
    [SerializeField] private string defaultServerIP;
    [SerializeField] private int defaultServerPort;

    [SerializeField] private bool startConnecting;

    [Header("UI for Comunication Info")]
    [SerializeField] private Text connTextField;

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
            TryToOpenCom(defaultServerIP, defaultServerPort);
        }
    }

    private void OnDestroy()
    {
        StopClient();
    }

    protected abstract void OpenCommunication(string ip, int port);
    protected abstract void CloseCommunication();
    protected abstract void SendData(byte[] data);
    protected abstract byte[] ReceiveResponse();
    protected abstract void UseResponseReceivedFromServer(byte[] response);

    public bool TryToOpenCom(string ip, int port)
    {
        if (connected)
        {
            Debug.Log("Already communicating to a server!");
            return false;
        }

        Debug.Log("Trying to establish communication with " + ip + "...");
        try
        {
            OpenCommunication(ip, port);
            Debug.Log("Communicating: " + ip);

            syncObj = new CommunicationSynchron();
            StartCoroutine(ReceivingRoutine());

            connected = true;
            return true;
        }
        catch (SocketException)
        {
            Debug.Log("Attempt refused!\n");

            connected = false;
            return false;
        }
        catch (Exception e)
        {
            Debug.Log("Fatal error during attempt! - " + e + "\n");

            connected = false;
            return false;
        }
    }

    protected virtual void StopClient()
    {
        Debug.Log("Stopping client...");

        CloseCommunication();
        connected = false;
    }

    protected void SendToServer(byte[] data)
    {
        SendData(data);

        lock (syncObj)
        {
            syncObj.recvBalance--;
            connTextField.text = specificConnectionInfo + "Balance: " + syncObj.recvBalance;
        }
    }

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
                    UseResponseReceivedFromServer(syncObj.recvData);
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
                byte[] responseData = ReceiveResponse();

                lock (syncObj)
                {
                    syncObj.recvData = responseData;
                    syncObj.recvFlag = true;
                    syncObj.recvBalance++;
                }
            }
        }
        catch (EndOfStreamException)
        {
            Debug.Log("Communication closed!\n");
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
}
