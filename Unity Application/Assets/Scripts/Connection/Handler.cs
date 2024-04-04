using System;
using UnityEngine;

[RequireComponent(typeof(Client))]
public abstract class Handler : MonoBehaviour
{
    [Header("Decoding Details")]
    [SerializeField] private char headerBodySeparator = '?';
    [SerializeField] private char inHeaderInfoSeparator = '|';
    [SerializeField] private char inBodyInstructionSeparator = '&';
    [SerializeField] private char inInstructionHandleValueSeparator = '=';

    public char HeaderBodySeparator { get => headerBodySeparator; }
    public char InHeaderInfoSeparator { get => inHeaderInfoSeparator; }
    public char InBodyInstructionSeparator { get => inBodyInstructionSeparator; }
    public char InInstructionHandleValueSeparator { get => inInstructionHandleValueSeparator; }

    public abstract void UseResponseReceivedFromServer(string response);
    public abstract void Shutdown();

    public event Action<byte[]> OnDataReady;
    protected void CallDataReadyEvent(byte[] data)
    {
        OnDataReady?.Invoke(data);
    }
}
