using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public abstract class InstructionReader : MonoBehaviour
{
    [SerializeField] private string handle;
    public string Handle { get => handle; }

    public abstract void SetDefault();
    public abstract void FollowInstruction(string instructionValue);
}
