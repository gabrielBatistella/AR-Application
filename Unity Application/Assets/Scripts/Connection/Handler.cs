using System;
using UnityEngine;

[RequireComponent(typeof(Client))]
public abstract class Handler : MonoBehaviour
{
    [Header("Decoding Details")]
    [SerializeField] private char detailsBodySeparator = '?';
    [SerializeField] private char inDetailsInfoSeparator = '|';

    public char DetailsBodySeparator { get => detailsBodySeparator; }
    public char InDetailsInfoSeparator { get => inDetailsInfoSeparator; }

    public abstract void UseResponseReceivedFromServer(string response);
    public abstract void Shutdown();

    public event Action<byte[]> OnDataReady;
    protected void CallDataReadyEvent(byte[] data)
    {
        OnDataReady?.Invoke(data);
    }
}
