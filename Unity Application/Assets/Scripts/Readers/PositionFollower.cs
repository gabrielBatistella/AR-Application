using System.Collections;
using System.Collections.Generic;
using System.Globalization;
using UnityEngine;

public class PositionFollower : InstructionReader
{
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

            string[] coordinates = instructionValue.Split(";");
            Vector3 position = new Vector3(float.Parse(coordinates[0], CultureInfo.InvariantCulture.NumberFormat), float.Parse(coordinates[1], CultureInfo.InvariantCulture.NumberFormat), float.Parse(coordinates[2], CultureInfo.InvariantCulture.NumberFormat));

            transform.position = position;
        }
    }
}
