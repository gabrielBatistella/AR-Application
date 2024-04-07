using System.Collections;
using System.Collections.Generic;
using UnityEngine;

[RequireComponent(typeof(LineRenderer))]
public class ElectrodeSetter : InstructionReader
{
    [SerializeField] private GameObject electrodePrefab;

    [SerializeField] private float reachDistance = 50f;

    [SerializeField] private Transform fixedParent;

    [SerializeField] private LayerMask layerGrabbable;

    private Ray aim;
    private LineRenderer aimLine;

    private void Awake()
    {
        aim = new Ray();
        aimLine = GetComponent<LineRenderer>();
    }

    protected override void InitSettings()
    {
        aim.origin = transform.position;
        aim.direction = transform.forward;
        aimLine.startColor = aimLine.endColor = Color.blue;

        gameObject.SetActive(false);
    }

    protected override void TurnSilent()
    {
        gameObject.SetActive(false);
    }

    protected override void FollowInstruction(string instructionValue)
    {
        if (instructionValue.StartsWith("Set"))
        {
            string[] pointsCoords = instructionValue.Split(":")[1].Split("/");

            transform.localPosition = PointFromCoords(pointsCoords[0].Split(";"));

            aim.origin = transform.position;
            aim.direction = (fixedParent.TransformPoint(PointFromCoords(pointsCoords[1].Split(";"))) - aim.origin).normalized;
            aimLine.SetPosition(0, transform.parent.InverseTransformPoint(aim.origin));
            aimLine.SetPosition(1, transform.parent.InverseTransformPoint(aim.origin + aim.direction * reachDistance));

            if (Physics.Raycast(aim.origin + aim.direction * reachDistance, -aim.direction, out RaycastHit hitInfo, reachDistance, layerGrabbable))
            {
                GameObject obj = Instantiate(electrodePrefab, transform.position, transform.rotation);
                obj.transform.SetParent(hitInfo.collider.gameObject.transform);

                ElectrodeInfoHandler electrodeInfo = obj.GetComponent<ElectrodeInfoHandler>();
                electrodeInfo.SetElectrode(transform.position, hitInfo.point);
                electrodeInfo.UpdateInfo();
            }
        }
        else
        {
            if (!gameObject.activeSelf)
            {
                gameObject.SetActive(true);
            }

            string[] pointsCoords = instructionValue.Split("/");

            transform.localPosition = PointFromCoords(pointsCoords[0].Split(";"));

            aim.origin = transform.position;
            aim.direction = (fixedParent.TransformPoint(PointFromCoords(pointsCoords[1].Split(";"))) - aim.origin).normalized;
            aimLine.SetPosition(0, transform.parent.InverseTransformPoint(aim.origin));
            aimLine.SetPosition(1, transform.parent.InverseTransformPoint(aim.origin + aim.direction * reachDistance));
        }
    }
}
