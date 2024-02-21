using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class TranslationTransformer : MonoBehaviour //InstructionReader
{
    [SerializeField] private Transform originTransform;
    [SerializeField] private LayerMask grabbableLayers;
    [SerializeField] private string nameOfLayerForGrabbed = "Grabbed";
    [SerializeField] private float reachDistance = 20f;

    private Ray aim;

    private GameObject grabbedObj;
    private Vector3 pointerPosWhenGrabbed;
    private Vector3 objPosWhenGrabbed;

    private void Awake()
    {
        aim = new Ray(originTransform.position, originTransform.forward);

        grabbedObj = null;
        pointerPosWhenGrabbed = Vector3.zero;
        objPosWhenGrabbed = Vector3.zero;
    }

    private void Update()
    {
        //aim.origin = cameraTransform.position;
        aim.direction = (transform.position - originTransform.position).normalized;
        
        if (grabbedObj != null)
        {
            Debug.DrawRay(aim.origin, aim.direction, Color.red, reachDistance);

            if (Physics.Raycast(aim, out RaycastHit hitInfo, reachDistance, LayerMask.NameToLayer(nameOfLayerForGrabbed)))
            {
                //grabbedObj.transform.localPosition = objPosWhenGrabbed + (transform.localPosition - pointerPosWhenGrabbed) * (hitInfo)
            }
        }
        else
        {
            Debug.DrawRay(aim.origin, aim.direction, Color.blue, reachDistance);
        }
    }

    public void TryGrabbing()
    {
        if (grabbedObj == null && Physics.Raycast(aim, out RaycastHit hitInfo, reachDistance))
        {

        }
    }

    public void Release()
    {
        grabbedObj = null;
        pointerPosWhenGrabbed = Vector3.zero;
        objPosWhenGrabbed = Vector3.zero;
    }
}
