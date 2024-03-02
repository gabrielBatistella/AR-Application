using System.Collections;
using System.Collections.Generic;
using UnityEngine;

[RequireComponent(typeof(LineRenderer))]
public class RotationCaster : InstructionReader
{
    [SerializeField] private float reachDistance = 50f;

    [SerializeField] private Transform freeParent;
    [SerializeField] private Transform fixedParent;

    [SerializeField] private LayerMask layerGrabbable;

    private Ray aim;
    private LineRenderer aimLine;

    private GameObject grabbedObj;
    private Vector3 objAngleWhenGrabbed;
    private Vector3 contactPointOnObject;

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

        grabbedObj = null;

        objAngleWhenGrabbed = Vector3.zero;
        contactPointOnObject = Vector3.zero;

        gameObject.SetActive(false);
    }

    public override void FollowInstruction(string instructionValue)
    {
        if (instructionValue == "Sem mao")
        {
            ReleaseIfHolding();
            gameObject.SetActive(false);
        }
        else if (instructionValue == "Soltar")
        {
            ReleaseIfHolding();
        }
        else if (instructionValue.StartsWith("Segurar"))
        {
            Vector3 targetPoint = pointFromCoords(instructionValue.Split(" ")[1].Split(";"));

            aim.direction = (fixedParent.TransformPoint(targetPoint) - aim.origin).normalized;
            aimLine.SetPosition(1, aim.origin + aim.direction * reachDistance);

            TryGrabbing(targetPoint);
        }
        else if (instructionValue.StartsWith("Segurando"))
        {
            if (grabbedObj != null)
            {
                Vector3 deltaAngle = pointFromCoords(instructionValue.Split(" ")[1].Split(";"));
                grabbedObj.transform.localEulerAngles = objAngleWhenGrabbed + deltaAngle;

                aimLine.SetPosition(1, grabbedObj.transform.TransformPoint(contactPointOnObject));
            }
            else
            {
                if (gameObject.activeSelf)
                {
                    gameObject.SetActive(false);
                }
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

    private void TryGrabbing(Vector3 targetPoint)
    {
        if (grabbedObj == null && Physics.Raycast(aim, out RaycastHit hitInfo, reachDistance, layerGrabbable))
        {
            grabbedObj = hitInfo.collider.gameObject;
            grabbedObj.transform.SetParent(fixedParent);

            objAngleWhenGrabbed = grabbedObj.transform.localEulerAngles;
            contactPointOnObject = grabbedObj.transform.InverseTransformPoint(hitInfo.point);

            aimLine.startColor = aimLine.endColor = Color.red;
        }
    }

    private void ReleaseIfHolding()
    {
        if (grabbedObj != null)
        {
            grabbedObj.transform.SetParent(freeParent);
            grabbedObj = null;

            objAngleWhenGrabbed = Vector3.zero;
            contactPointOnObject = Vector3.zero;

            aimLine.startColor = aimLine.endColor = Color.blue;
        }
    }
}