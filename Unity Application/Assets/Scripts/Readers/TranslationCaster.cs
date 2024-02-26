using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class TranslationCaster : MonoBehaviour //InstructionReader
{
    [SerializeField] private float reachDistance = 20f;

    [SerializeField] private Transform originTransform;
    [SerializeField] private LineRenderer aimLine;

    [SerializeField] private Transform freeParent;
    [SerializeField] private Transform fixedParent;

    [SerializeField] private LayerMask layerGrabbable;

    private Ray aim;

    private GameObject grabbedObj;
    private Vector3 pointerPosWhenGrabbed;
    private Vector3 objPosWhenGrabbed;
    private float pointerObjTranslationRatio;

    private void Awake()
    {
        aim = new Ray(originTransform.position, originTransform.forward);
        aimLine.startColor = aimLine.endColor = Color.blue;

        grabbedObj = null;

        pointerPosWhenGrabbed = Vector3.zero;
        objPosWhenGrabbed = Vector3.zero;
        pointerObjTranslationRatio = 0;
    }

    private void Update()
    {
        //aim.origin = originTransform.position;
        aim.direction = (transform.position - originTransform.position).normalized;
        
        if (grabbedObj != null)
        {
            grabbedObj.transform.localPosition = objPosWhenGrabbed + (transform.localPosition - pointerPosWhenGrabbed) * pointerObjTranslationRatio;
            aimLine.SetPosition(1, aim.origin + aim.direction * transform.localPosition.magnitude * pointerObjTranslationRatio);
        }
        else
        {
            aimLine.SetPosition(1, aim.origin + aim.direction * reachDistance);
        }
    }

    public void TryGrabbing()
    {
        if (grabbedObj == null && Physics.Raycast(aim, out RaycastHit hitInfo, reachDistance, layerGrabbable))
        {
            grabbedObj = hitInfo.collider.gameObject;
            grabbedObj.transform.SetParent(fixedParent);

            pointerPosWhenGrabbed = transform.localPosition;
            objPosWhenGrabbed = grabbedObj.transform.localPosition;
            pointerObjTranslationRatio = fixedParent.InverseTransformPoint(hitInfo.point).magnitude / transform.localPosition.magnitude;

            aimLine.startColor = aimLine.endColor = Color.red;
        }
    }

    public void Release()
    {
        if (grabbedObj != null)
        {
            grabbedObj.transform.SetParent(freeParent);
            grabbedObj = null;

            pointerPosWhenGrabbed = Vector3.zero;
            objPosWhenGrabbed = Vector3.zero;
            pointerObjTranslationRatio = 0;

            aimLine.startColor = aimLine.endColor = Color.blue;
        }
    }
}
