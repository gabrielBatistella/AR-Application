using System.Collections;
using System.Collections.Generic;
using System.Text;
using UnityEngine;
using UnityEngine.UI;

public class VCraniumClient : TCPClient
{
    [Header("Image Details")]
    [SerializeField] private CameraVision cam;
    [SerializeField] private int imageQuality = 75;
    [SerializeField] private int maxFPS = 60;

    [Header("Decoding Details")]
    [SerializeField] private char headerBodySeparator = '?';
    [SerializeField] private char inHeaderInfoSeparator = '|';
    [SerializeField] private char inBodyInstructionSeparator = '&';
    [SerializeField] private char inInstructionHandleValueSeparator = '=';

    [Header("UI for Header Info")]
    [SerializeField] private Text headerTextField;

    [Header("Instruction Readers")]
    [SerializeField] private List<InstructionReader> readers;

    private float nextFrameTime = 0;

    protected override void Start()
    {
        base.Start();
        foreach (InstructionReader reader in readers)
        {
            reader.SetDefault();
        }
    }

    private void Update()
    {
        if (Connected && Time.time > nextFrameTime)
        {
            nextFrameTime = Time.time + 1f / maxFPS;
            SendToServer(cam.GetFrameJPG(imageQuality));
        }
    }

    protected override void UseDataReceivedFromServer(byte[] data)
    {
        string textData = Encoding.UTF8.GetString(data, 0, data.Length);
        string[] headerBody = textData.Split(headerBodySeparator);

        ShowHeaderInfo(headerBody[0]);
        HandleBodyInstructions(headerBody[1]);
    }

    private void ShowHeaderInfo(string header)
    {
        string[] infos = header.Split(inHeaderInfoSeparator);
        string headerText = "";
        foreach (string info in infos)
        {
            headerText += info + "\n";
        }
        headerTextField.text = headerText;
    }

    private void HandleBodyInstructions(string body)
    {
        string[] instructions = body.Split(inBodyInstructionSeparator);
        foreach (string instruction in instructions)
        {
            string[] handleValue = instruction.Split(inInstructionHandleValueSeparator);
            readers.Find(reader => reader.Handle == handleValue[0])?.FollowInstruction(handleValue[1]);
        }
    }

    protected override void StopClient()
    {
        base.StopClient();
        Destroy(gameObject);
    }
}
