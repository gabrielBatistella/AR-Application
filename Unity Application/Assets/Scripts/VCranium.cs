using System.Collections.Generic;
using System.Linq;
using UnityEngine;

public class VCranium : Handler
{
    [Header("Image Parameters")]
    [SerializeField] private CameraVision cam;
    [SerializeField] private int imageQuality = 75;
    [SerializeField] private int maxFPS = 60;

    [Header("Instruction Readers")]
    [SerializeField] private List<InstructionReader> readers;

    private float nextFrameTime = 0;

    private void Start()
    {
        client.OnClientStop += Shutdown;

        foreach (InstructionReader reader in readers)
        {
            reader.SetDefault();
        }
    }

    private void Update()
    {
        if (client.Connected && Time.time > nextFrameTime)
        {
            nextFrameTime = Time.time + 1f / maxFPS;
            client.SendToServer(cam.GetFrameJPG(imageQuality));
        }
    }

    public override void UseResponseReceivedFromServer(string response)
    {
        IEnumerable<(string Handle, string Value)> instructions = response.Split(InBodyInstructionSeparator).Select(instruction =>
        {
            if (!string.IsNullOrEmpty(instruction))
            {
                string[] parsedInstruction = instruction.Split(InInstructionHandleValueSeparator);
                return (Handle: parsedInstruction[0], Value: parsedInstruction[1]);
            }
            else
            {
                return default;
            }
        });

        foreach (InstructionReader reader in readers)
        {
            (string Handle, string Value) instructionFound = instructions.FirstOrDefault(instruction => instruction.Handle == reader.Handle);
            if (instructionFound != default)
            {
                reader.ReadInstruction(instructionFound.Value);
            }
            else
            {
                reader.SetSilent();
            }
        }
    }

    private void Shutdown()
    {
        Destroy(gameObject);
    }
}
