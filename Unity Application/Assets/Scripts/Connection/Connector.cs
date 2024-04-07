using System;
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

    protected byte[] Int2Bytes(int value)
    {
        byte[] bytes = BitConverter.GetBytes(value);
        if (BitConverter.IsLittleEndian)
            Array.Reverse(bytes);
        return bytes;
    }

    protected byte[] Short2Bytes(short value)
    {
        byte[] bytes = BitConverter.GetBytes(value);
        if (BitConverter.IsLittleEndian)
            Array.Reverse(bytes);
        return bytes;
    }

    protected int Bytes2Int(byte[] bytes)
    {
        if (BitConverter.IsLittleEndian)
            Array.Reverse(bytes);
        int value = BitConverter.ToInt32(bytes);
        return value;
    }

    protected short Bytes2Short(byte[] bytes)
    {
        if (BitConverter.IsLittleEndian)
            Array.Reverse(bytes);
        short value = BitConverter.ToInt16(bytes);
        return value;
    }
}
