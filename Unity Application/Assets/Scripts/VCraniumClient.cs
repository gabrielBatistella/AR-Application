using System.Collections;
using System.Collections.Generic;
using System.Text;
using UnityEngine;

public class VCraniumClient : TCPClient
{
    [SerializeField] private string message;

    // Update is called once per frame
    void Update()
    {
        if (Input.GetKeyDown(KeyCode.Space))
        {
            SendToServer(Encoding.UTF8.GetBytes(message));
        }
    }

    protected override void UseDataReceivedFromServer(byte[] data)
    {
        string text = Encoding.UTF8.GetString(data, 0, data.Length);
        Debug.Log(text);
    }

    protected override void StopClient()
    {
        base.StopClient();

        Destroy(gameObject);
    }
}
