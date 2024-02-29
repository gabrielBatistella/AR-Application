using System.Collections;
using System.Collections.Generic;
using System.Globalization;
using UnityEngine;

public abstract class InstructionReader : MonoBehaviour
{
    [SerializeField] private string handle;
    public string Handle { get => handle; }

    public abstract void SetDefault();
    public abstract void FollowInstruction(string instructionValue);

    protected Vector3 pointFromCoords(string[] coordinates)
    {
        return new Vector3(float.Parse(coordinates[0], CultureInfo.InvariantCulture.NumberFormat), float.Parse(coordinates[1], CultureInfo.InvariantCulture.NumberFormat), float.Parse(coordinates[2], CultureInfo.InvariantCulture.NumberFormat));
    }
}