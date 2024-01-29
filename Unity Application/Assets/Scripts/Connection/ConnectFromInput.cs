using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

[RequireComponent(typeof(TCPClient))]
public class ConnectFromInput : MonoBehaviour
{
    [SerializeField] private InputField ipInput;
    [SerializeField] private InputField portInput;

    [SerializeField] private GameObject errorMessage;
    [SerializeField] private GameObject inputUI;

    private TCPClient client;

    private void Awake()
    {
        client = GetComponent<TCPClient>();
    }

    public void TryConnecting()
    {
        bool ok = client.TryToConnect(ipInput.text, int.Parse(portInput.text));

        if (ok)
        {
            errorMessage.SetActive(false);
            inputUI.SetActive(false);
        }
        else
        {
            errorMessage.SetActive(true);
        }
    }
}
