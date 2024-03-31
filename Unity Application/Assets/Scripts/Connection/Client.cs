using System;
using System.IO;
using System.Net.Sockets;
using UnityEngine;
using System.Collections;
using System.Threading;
using UnityEngine.UI;
using System.Text;

[RequireComponent(typeof(Connector))]
[RequireComponent(typeof(Handler))]
public class Client : MonoBehaviour
{
    [Header("Server Info")]
    [SerializeField] private string defaultServerIP;
    [SerializeField] private int defaultServerPort;

    [SerializeField] private bool startConnecting;

    [Header("UI for Communication Info")]
    [SerializeField] private Text connTextField;

    private CommunicationSynchron syncObj;
    private Connector connector;
    private Handler handler;

    private bool connected = false;
    public bool Connected { get => connected; }

    private class CommunicationSynchron
    {
        public byte[] recvData = null;
        public bool recvFlag = false;
        public int recvBalance = 0;

        public bool comDown = false;
    }

    private void Awake()
    {
        connector = GetComponent<Connector>();
        handler = GetComponent<Handler>();
    }

    private void Start()
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
            connector.OpenCommunication(ip, port);
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

    public event Action OnClientStop;
    private void StopClient()
    {
        if (connected)
        {
            Debug.Log("Stopping client...");

            connector.CloseCommunication();
            connected = false;

            OnClientStop?.Invoke();
        }
    }

    public void SendToServer(byte[] data)
    {
        connector.SendData(data);

        lock (syncObj)
        {
            syncObj.recvBalance--;
        }
    }

    private IEnumerator ReceivingRoutine()
    {
        Thread receivingThread = new Thread(ReceivingFromServer);
        receivingThread.Start();

        while (true)
        {
            byte[] response = null;
            lock (syncObj)
            {
                if (syncObj.comDown)
                {
                    StopClient();
                    yield break;
                }
                else if (syncObj.recvFlag)
                {
                    response = syncObj.recvData;
                    syncObj.recvFlag = false;
                }
            }

            if (response != null)
            {
                string textData = Encoding.UTF8.GetString(response, 0, response.Length);
                string[] headerBody = textData.Split(handler.HeaderBodySeparator);

                ShowHeaderInfo(headerBody[0]);
                handler.UseResponseReceivedFromServer(headerBody[1]);
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
                byte[] responseData = connector.ReceiveResponse();

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

    private void ShowHeaderInfo(string header)
    {
        string[] infos = header.Split(handler.InHeaderInfoSeparator);
        string headerText = "";
        foreach (string info in infos)
        {
            headerText += info + "\n";
        }

        string balanceText = "";
        lock (syncObj)
        {
            balanceText = "Balance: " + syncObj.recvBalance;
        }

        connTextField.text = headerText + balanceText;
    }
}
