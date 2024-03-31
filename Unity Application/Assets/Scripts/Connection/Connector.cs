using UnityEngine;

[RequireComponent(typeof(Client))]
public abstract class Connector : MonoBehaviour
{
    [Header("Encoding Details")]
    [SerializeField] private int headerSize = 16;

    public int HeaderSize { get => headerSize; }

    public abstract void OpenCommunication(string ip, int port);
    public abstract void CloseCommunication();
    public abstract void SendData(byte[] data);
    public abstract byte[] ReceiveResponse();
}
