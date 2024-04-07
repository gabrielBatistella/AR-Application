using System.Collections;
using System.Collections.Generic;
using UnityEngine;

[RequireComponent(typeof(LineRenderer))]
public class Test : MonoBehaviour
{
    public Transform testTarget;

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

    private void Start()
    {
        aim.origin = transform.position;
        aim.direction = transform.forward;
        aimLine.startColor = aimLine.endColor = Color.cyan;
    }

    private void Update()
    {
        aim.origin = transform.position;
        aim.direction = (fixedParent.TransformPoint(testTarget.localPosition) - aim.origin).normalized;
        aimLine.SetPosition(0, transform.parent.InverseTransformPoint(aim.origin));
        aimLine.SetPosition(1, transform.parent.InverseTransformPoint(aim.origin + aim.direction * reachDistance));
    }

    public void TestThis()
    {
        if (Physics.Raycast(aim.origin + aim.direction * reachDistance, -aim.direction, out RaycastHit hitInfo, reachDistance, layerGrabbable))
        {
            GameObject obj = Instantiate(electrodePrefab, transform.position, transform.rotation);
            obj.transform.SetParent(hitInfo.collider.gameObject.transform);

            ElectrodeInfoHandler electrodeInfo = obj.GetComponent<ElectrodeInfoHandler>();
            electrodeInfo.SetElectrode(transform.position, hitInfo.point);
            electrodeInfo.UpdateInfo();
        }
    }
}

