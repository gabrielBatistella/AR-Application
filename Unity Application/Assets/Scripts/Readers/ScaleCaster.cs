using System.Globalization;
using UnityEngine;

[RequireComponent(typeof(LineRenderer))]
public class ScaleCaster : InstructionReader
{
    [SerializeField] private float reachDistance = 50f;

    [SerializeField] private Transform freeParent;
    [SerializeField] private Transform fixedParent;

    [SerializeField] private LayerMask layerGrabbable;

    private Ray aim;
    private LineRenderer aimLine;

    private GameObject grabbedObj;
    private Vector3 objSizeWhenGrabbed;
    private Vector3 contactPointOnObject;

    private void Awake()
    {
        aim = new Ray();
        aimLine = GetComponent<LineRenderer>();
    }

    protected override void InitSettings()
    {
        aim.origin = transform.position;
        aim.direction = transform.forward;
        aimLine.startColor = aimLine.endColor = Color.yellow;

        grabbedObj = null;

        objSizeWhenGrabbed = Vector3.zero;
        contactPointOnObject = Vector3.zero;

        gameObject.SetActive(false);
    }

    protected override void TurnSilent()
    {
        ReleaseIfHolding();
        gameObject.SetActive(false);
    }

    protected override void FollowInstruction(string instructionValue)
    {
        if (instructionValue.StartsWith("Grab"))
        {
            Vector3 targetPoint = PointFromCoords(instructionValue.Split(":")[1].Split(";"));

            aim.direction = (fixedParent.TransformPoint(targetPoint) - aim.origin).normalized;
            aimLine.SetPosition(1, transform.parent.InverseTransformPoint(aim.origin + aim.direction * reachDistance));

            TryGrabbing(targetPoint);
        }
        else if (instructionValue.StartsWith("Release"))
        {
            ReleaseIfHolding();

            Vector3 targetPoint = PointFromCoords(instructionValue.Split(":")[1].Split(";"));

            aim.direction = (fixedParent.TransformPoint(targetPoint) - aim.origin).normalized;
            aimLine.SetPosition(1, transform.parent.InverseTransformPoint(aim.origin + aim.direction * reachDistance));
        }
        else if (instructionValue.StartsWith("Holding"))
        {
            if (grabbedObj != null)
            {
                if (!gameObject.activeSelf)
                {
                    gameObject.SetActive(true);
                }

                float sizeFactor = float.Parse(instructionValue.Split(":")[1], CultureInfo.InvariantCulture.NumberFormat);
                grabbedObj.transform.localScale = objSizeWhenGrabbed * sizeFactor;

                aimLine.SetPosition(1, transform.parent.InverseTransformPoint(grabbedObj.transform.TransformPoint(contactPointOnObject)));
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

            aim.direction = (fixedParent.TransformPoint(PointFromCoords(instructionValue.Split(";"))) - aim.origin).normalized;
            aimLine.SetPosition(1, transform.parent.InverseTransformPoint(aim.origin + aim.direction * reachDistance));
        }
    }

    private void TryGrabbing(Vector3 targetPoint)
    {
        if (grabbedObj == null && Physics.Raycast(aim, out RaycastHit hitInfo, reachDistance, layerGrabbable))
        {
            grabbedObj = hitInfo.collider.gameObject;
            grabbedObj.transform.SetParent(fixedParent);

            objSizeWhenGrabbed = grabbedObj.transform.localScale;
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

            objSizeWhenGrabbed = Vector3.zero;
            contactPointOnObject = Vector3.zero;

            aimLine.startColor = aimLine.endColor = Color.yellow;
        }
    }
}