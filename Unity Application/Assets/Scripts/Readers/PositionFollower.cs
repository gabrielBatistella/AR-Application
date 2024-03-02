using System.Collections;
using System.Collections.Generic;
using System.Globalization;
using UnityEngine;

public class PositionFollower : InstructionReader
{
    [SerializeField] private List<Transform> objPoints;

    public override void SetDefault()
    {
        gameObject.SetActive(false);
    }

    public override void FollowInstruction(string instructionValue)
    {
        if (instructionValue == "Lost Track")
        {
            gameObject.SetActive(false);
        }
        else
        {
            if (!gameObject.activeSelf)
            {
                gameObject.SetActive(true);
            }

            string[] coordsOfObjPoints = instructionValue.Split("/");
            for (int i = 0; i < coordsOfObjPoints.Length; i++)
            {
                objPoints[i].localPosition = pointFromCoords(coordsOfObjPoints[i].Split(";"));
            }
        }
    }
}