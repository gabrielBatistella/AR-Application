using UnityEngine;
using UnityEngine.UI;

[RequireComponent(typeof(Client))]
public class ConnectFromInput : MonoBehaviour
{
    [SerializeField] private InputField ipInput;
    [SerializeField] private InputField portInput;

    [SerializeField] private GameObject errorMessage;
    [SerializeField] private GameObject inputUI;

    private Client client;

    private void Awake()
    {
        client = GetComponent<Client>();
    }

    public void TryConnecting()
    {
        bool ok = client.TryToOpenCom(ipInput.text, int.Parse(portInput.text));

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
