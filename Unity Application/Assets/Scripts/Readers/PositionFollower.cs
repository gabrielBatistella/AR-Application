using System.Collections.Generic;
using UnityEngine;

public class PositionFollower : InstructionReader
{
    [SerializeField] private List<Transform> objPoints;

    protected override void InitSettings()
    {
        gameObject.SetActive(false);
    }

    protected override void TurnSilent()
    {
        gameObject.SetActive(false);
    }

    protected override void FollowInstruction(string instructionValue)
    {
        if (!gameObject.activeSelf)
        {
            gameObject.SetActive(true);
        }

        string[] coordsOfObjPoints = instructionValue.Split("/");
        for (int i = 0; i < coordsOfObjPoints.Length; i++)
        {
            objPoints[i].localPosition = PointFromCoords(coordsOfObjPoints[i].Split(";"));
        }
    }
}