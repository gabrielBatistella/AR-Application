using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class FreeTransformCaster : InstructionReader
{
    [SerializeField] private float reachDistance = 50f;

    [SerializeField] private LineRenderer[] aimLines;

    [SerializeField] private Transform freeParent;
    [SerializeField] private Transform fixedParent;

    [SerializeField] private LayerMask layerGrabbable;

    private Ray[] aims;

    private GameObject[] grabbedObjs;
    private Vector3[] pointersPosWhenGrabbed;
    private Vector3[] objsPosWhenGrabbed;
    private Quaternion[] objsAngleWhenGrabbed;
    private Vector3[] objsSizeWhenGrabbed;
    private Vector3[] contactPointsOnObject;
    private float[] pointerObjTranslationRatios;

    private void Awake()
    {
        aims = new Ray[2];

        grabbedObjs = new GameObject[2];
        pointersPosWhenGrabbed = new Vector3[2];
        objsPosWhenGrabbed = new Vector3[2];
        objsAngleWhenGrabbed = new Quaternion[2];
        objsSizeWhenGrabbed = new Vector3[2];
        contactPointsOnObject = new Vector3[2];
        pointerObjTranslationRatios = new float[2];
    }

    public override void SetDefault()
    {
        for (int i = 0; i < 2; i++)
        {
            aims[i].origin = transform.position;
            aims[i].direction = transform.forward;
            aimLines[i].startColor = aimLines[i].endColor = Color.blue;

            grabbedObjs[i] = null;

            pointersPosWhenGrabbed[i] = Vector3.zero;
            objsPosWhenGrabbed[i] = Vector3.zero;
            objsAngleWhenGrabbed[i] = Quaternion.identity;
            objsSizeWhenGrabbed[i] = Vector3.zero;
            contactPointsOnObject[i] = Vector3.zero;
            pointerObjTranslationRatios[i] = 0;

            aimLines[i].gameObject.SetActive(false);
        }
    }

    public override void FollowInstruction(string instructionValue)
    {
        string[] instructions = instructionValue.Split("/");
        for (int i = 0; i < 2; i++)
        {
            if (instructions[i] == "None")
            {

            }
            else if (instructions[i] == "Lost Track")
            {
                if (grabbedObjs[i] != null && grabbedObjs[(i + 1) % 2] == grabbedObjs[i] && instructions[(i + 1) % 2].StartsWith("Segurando"))
                {
                    Vector3 targetPointOther = pointFromCoords(instructions[(i + 1) % 2].Split(":")[1].Split(";"));

                    aims[(i + 1) % 2].direction = (fixedParent.TransformPoint(targetPointOther) - aims[(i + 1) % 2].origin).normalized;
                    aimLines[(i + 1) % 2].SetPosition(1, aims[(i + 1) % 2].origin + aims[(i + 1) % 2].direction * reachDistance);

                    TryGrabbing((i + 1) % 2, targetPointOther);
                }

                ReleaseIfHolding(i);
                aimLines[i].gameObject.SetActive(false);
            }
            else if (instructions[i].StartsWith("Grab"))
            {
                Vector3 targetPoint = pointFromCoords(instructions[i].Split(":")[1].Split(";"));

                aims[i].direction = (fixedParent.TransformPoint(targetPoint) - aims[i].origin).normalized;
                aimLines[i].SetPosition(1, aims[i].origin + aims[i].direction * reachDistance);

                TryGrabbing(i, targetPoint);

                if (grabbedObjs[i] != null && grabbedObjs[(i + 1) % 2] == grabbedObjs[i] && instructions[(i + 1) % 2].StartsWith("Holding"))
                {
                    Vector3 targetPointOther = pointFromCoords(instructions[(i + 1) % 2].Split(":")[1].Split(";"));

                    aims[(i + 1) % 2].direction = (fixedParent.TransformPoint(targetPointOther) - aims[(i + 1) % 2].origin).normalized;
                    aimLines[(i + 1) % 2].SetPosition(1, aims[(i + 1) % 2].origin + aims[(i + 1) % 2].direction * reachDistance);

                    TryGrabbing((i + 1) % 2, targetPointOther);
                }
            }
            else if (instructionValue.StartsWith("Release"))
            {
                if (grabbedObjs[i] != null && grabbedObjs[(i + 1) % 2] == grabbedObjs[i] && instructions[(i + 1) % 2].StartsWith("Holding"))
                {
                    Vector3 targetPointOther = pointFromCoords(instructions[(i + 1) % 2].Split(":")[1].Split(";"));

                    aims[(i + 1) % 2].direction = (fixedParent.TransformPoint(targetPointOther) - aims[(i + 1) % 2].origin).normalized;
                    aimLines[(i + 1) % 2].SetPosition(1, aims[(i + 1) % 2].origin + aims[(i + 1) % 2].direction * reachDistance);

                    TryGrabbing((i + 1) % 2, targetPointOther);
                }

                ReleaseIfHolding(i);

                Vector3 targetPoint = pointFromCoords(instructions[i].Split(":")[1].Split(";"));

                aims[i].direction = (fixedParent.TransformPoint(targetPoint) - aims[i].origin).normalized;
                aimLines[i].SetPosition(1, aims[i].origin + aims[i].direction * reachDistance);
            }
            else if (instructions[i].StartsWith("Holding"))
            {
                if (grabbedObjs[i] != null)
                {
                    if (grabbedObjs[(i + 1) % 2] == grabbedObjs[i] && instructions[(i + 1) % 2].StartsWith("Holding"))
                    {
                        if (i == 0)
                        {
                            Vector3 targetPoint1 = pointFromCoords(instructions[0].Split(":")[1].Split(";"));
                            Vector3 targetPoint2 = pointFromCoords(instructions[1].Split(":")[1].Split(";"));

                            Vector3 deltaPos = (targetPoint1 + targetPoint2) / 2 - (pointersPosWhenGrabbed[0] + pointersPosWhenGrabbed[1]) / 2;
                            Quaternion deltaAngle = Quaternion.FromToRotation((pointersPosWhenGrabbed[1] - pointersPosWhenGrabbed[0]).normalized, (targetPoint2 - targetPoint1).normalized);
                            float sizeFactor = (targetPoint2 - targetPoint1).magnitude / (pointersPosWhenGrabbed[1] - pointersPosWhenGrabbed[0]).magnitude;

                            grabbedObjs[0].transform.localPosition = objsPosWhenGrabbed[0] + deltaPos * (pointerObjTranslationRatios[0] + pointerObjTranslationRatios[1]) / 2;
                            grabbedObjs[0].transform.localRotation = objsAngleWhenGrabbed[0] * deltaAngle;
                            grabbedObjs[0].transform.localScale = objsSizeWhenGrabbed[0] * sizeFactor;
                        }
                    }
                    else
                    {
                        Vector3 deltaPos = pointFromCoords(instructions[i].Split(":")[1].Split(";")) - pointersPosWhenGrabbed[i];
                        grabbedObjs[i].transform.localPosition = objsPosWhenGrabbed[i] + deltaPos * pointerObjTranslationRatios[i];
                    }
                    aimLines[i].SetPosition(1, grabbedObjs[i].transform.TransformPoint(contactPointsOnObject[i]));
                }
                else
                {
                    if (aimLines[i].gameObject.activeSelf)
                    {
                        aimLines[i].gameObject.SetActive(false);
                    }
                }
            }
            else
            {
                if (!aimLines[i].gameObject.activeSelf)
                {
                    aimLines[i].gameObject.SetActive(true);
                }

                aims[i].direction = (fixedParent.TransformPoint(pointFromCoords(instructions[i].Split(";"))) - aims[i].origin).normalized;
                aimLines[i].SetPosition(1, aims[i].origin + aims[i].direction * reachDistance);
            }
        }
    }

    private void TryGrabbing(int index, Vector3 targetPoint)
    {
        if (grabbedObjs[index] == null && Physics.Raycast(aims[index], out RaycastHit hitInfo, reachDistance, layerGrabbable))
        {
            grabbedObjs[index] = hitInfo.collider.gameObject;
            grabbedObjs[index].transform.SetParent(fixedParent);

            pointersPosWhenGrabbed[index] = targetPoint;
            objsPosWhenGrabbed[index] = grabbedObjs[index].transform.localPosition;
            objsAngleWhenGrabbed[index] = grabbedObjs[index].transform.localRotation;
            objsSizeWhenGrabbed[index] = grabbedObjs[index].transform.localScale;
            contactPointsOnObject[index] = grabbedObjs[index].transform.InverseTransformPoint(hitInfo.point);
            pointerObjTranslationRatios[index] = fixedParent.InverseTransformPoint(hitInfo.point).magnitude / targetPoint.magnitude;

            aimLines[index].startColor = aimLines[index].endColor = Color.red;
        }
    }

    private void ReleaseIfHolding(int index)
    {
        if (grabbedObjs[index] != null)
        {
            grabbedObjs[index].transform.SetParent(freeParent);
            grabbedObjs[index] = null;

            pointersPosWhenGrabbed[index] = Vector3.zero;
            objsPosWhenGrabbed[index] = Vector3.zero;
            objsAngleWhenGrabbed[index] = Quaternion.identity;
            objsSizeWhenGrabbed[index] = Vector3.zero;
            contactPointsOnObject[index] = Vector3.zero;
            pointerObjTranslationRatios[index] = 0;

            aimLines[index].startColor = aimLines[index].endColor = Color.blue;
        }
    }
}