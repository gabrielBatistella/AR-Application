using UnityEngine;

[RequireComponent(typeof(Client))]
public abstract class Handler : MonoBehaviour
{
    [Header("Decoding Details")]
    [SerializeField] private char headerBodySeparator = '?';
    [SerializeField] private char inHeaderInfoSeparator = '|';
    [SerializeField] private char inBodyInstructionSeparator = '&';
    [SerializeField] private char inInstructionHandleValueSeparator = '=';

    protected Client client;

    public char HeaderBodySeparator { get => headerBodySeparator; }
    public char InHeaderInfoSeparator { get => inHeaderInfoSeparator; }
    public char InBodyInstructionSeparator { get => inBodyInstructionSeparator; }
    public char InInstructionHandleValueSeparator { get => inInstructionHandleValueSeparator; }

    protected virtual void Awake()
    {
        client = GetComponent<Client>();
    }

    public abstract void UseResponseReceivedFromServer(string response);
}
