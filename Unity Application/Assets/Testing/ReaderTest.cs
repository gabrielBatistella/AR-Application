using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class ReaderTest : InstructionReader
{
    public override void SetDefault()
    {
        
    }

    public override void FollowInstruction(string instructionValue)
    {
        Debug.Log(instructionValue);
    }
}
