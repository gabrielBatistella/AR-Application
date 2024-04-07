using System.Collections.Generic;
using UnityEngine;

public class PoseFollower : InstructionReader
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

        string[] posesOfObjPoints = instructionValue.Split("/");
        for (int i = 0; i < posesOfObjPoints.Length; i++)
        {
            string[] pose = posesOfObjPoints[i].Split(";");
            objPoints[i].localPosition = PointFromCoords(pose[..3]);
            objPoints[i].localEulerAngles = PointFromCoords(pose[3..]);
        }
    }
}