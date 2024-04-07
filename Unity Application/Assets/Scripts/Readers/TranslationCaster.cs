using UnityEngine;

[RequireComponent(typeof(LineRenderer))]
public class TranslationCaster : InstructionReader
{
    [SerializeField] private float reachDistance = 50f;

    [SerializeField] private Transform freeParent;
    [SerializeField] private Transform fixedParent;

    [SerializeField] private LayerMask layerGrabbable;

    private Ray aim;
    private LineRenderer aimLine;

    private GameObject grabbedObj;
    private Vector3 objPosWhenGrabbed;
    private Vector3 contactPointOnObject;
    private float pointerObjTranslationRatio;

    private void Awake()
    {
        aim = new Ray();
        aimLine = GetComponent<LineRenderer>();
    }

    protected override void InitSettings()
    {
        aim.origin = transform.position;
        aim.direction = transform.forward;
        aimLine.startColor = aimLine.endColor = Color.black;

        grabbedObj = null;

        objPosWhenGrabbed = Vector3.zero;
        contactPointOnObject = Vector3.zero;
        pointerObjTranslationRatio = 0;

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
                Vector3 deltaPos = PointFromCoords(instructionValue.Split(":")[1].Split(";"));
                grabbedObj.transform.localPosition = objPosWhenGrabbed + deltaPos * pointerObjTranslationRatio;

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

            objPosWhenGrabbed = grabbedObj.transform.localPosition;
            contactPointOnObject = grabbedObj.transform.InverseTransformPoint(hitInfo.point);
            pointerObjTranslationRatio = fixedParent.InverseTransformPoint(hitInfo.point).magnitude / targetPoint.magnitude;

            aimLine.startColor = aimLine.endColor = Color.red;
        }
    }

    private void ReleaseIfHolding()
    {
        if (grabbedObj != null)
        {
            grabbedObj.transform.SetParent(freeParent);
            grabbedObj = null;

            objPosWhenGrabbed = Vector3.zero;
            contactPointOnObject = Vector3.zero;
            pointerObjTranslationRatio = 0;

            aimLine.startColor = aimLine.endColor = Color.black;
        }
    }
}