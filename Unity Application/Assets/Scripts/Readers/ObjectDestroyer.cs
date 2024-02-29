using System.Collections;
using System.Collections.Generic;
using System.Globalization;
using UnityEngine;

[RequireComponent(typeof(LineRenderer))]
public class ObjectDestroyer : InstructionReader
{
    [SerializeField] private float reachDistance = 20f;

    [SerializeField] private Transform freeParent;
    [SerializeField] private Transform fixedParent;

    [SerializeField] private LayerMask layerGrabbable;

    private Ray aim;
    private LineRenderer aimLine;

    private void Awake()
    {
        aim = new Ray();
        aimLine = GetComponent<LineRenderer>();
    }

    public override void SetDefault()
    {
        aim.origin = transform.position;
        aim.direction = transform.forward;
        aimLine.startColor = aimLine.endColor = Color.blue;

        gameObject.SetActive(false);
    }

    public override void FollowInstruction(string instructionValue)
    {
        if (instructionValue == "Sem mao")
        {
            gameObject.SetActive(false);
        }
        else if (instructionValue.StartsWith("Deletar"))
        {
            Vector3 targetPoint = pointFromCoords(instructionValue.Split(" ")[1].Split(";"));

            aim.direction = (fixedParent.TransformPoint(targetPoint) - aim.origin).normalized;
            aimLine.SetPosition(1, aim.origin + aim.direction * reachDistance);

            if (Physics.Raycast(aim, out RaycastHit hitInfo, reachDistance, layerGrabbable))
            {
                Destroy(hitInfo.collider.gameObject);
            }
        }
        else
        {
            if (!gameObject.activeSelf)
            {
                gameObject.SetActive(true);
            }

            aim.direction = (fixedParent.TransformPoint(pointFromCoords(instructionValue.Split(";"))) - aim.origin).normalized;
            aimLine.SetPosition(1, aim.origin + aim.direction * reachDistance);
        }
    }
}