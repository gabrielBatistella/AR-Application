using System.Globalization;
using UnityEngine;

public abstract class InstructionReader : MonoBehaviour
{
    [SerializeField] private string handle;

    private bool silent;

    public string Handle { get => handle; }

    public void SetDefault()
    {
        InitSettings();
        silent = true;
    }

    public void SetSilent()
    {
        if (!silent)
        {
            TurnSilent();
            silent = true;
        }
    }

    public void ReadInstruction(string instructionValue)
    {
        FollowInstruction(instructionValue);
        silent = false;
    }

    protected abstract void InitSettings();
    protected abstract void TurnSilent();
    protected abstract void FollowInstruction(string instructionValue);

    protected Vector3 PointFromCoords(string[] coordinates)
    {
        return new Vector3(float.Parse(coordinates[0], CultureInfo.InvariantCulture.NumberFormat), float.Parse(coordinates[1], CultureInfo.InvariantCulture.NumberFormat), float.Parse(coordinates[2], CultureInfo.InvariantCulture.NumberFormat));
    }
}